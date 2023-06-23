import json

import grpc
import utilities_pb2 as util
import utilities_pb2_grpc as util_grpc
import order_pb2 as ord
import order_pb2_grpc as ord_grpc
from threading import Thread
import market_data_pb2 as md
import market_data_pb2_grpc as md_grpc
import time
import uuid
import datetime
import pytz
import holidays
import logging
import os
import getpass
import dotenv
import pandas as pd

from bracket_order import OrderDirection
from bracket_order import OrderType
from bracket_order import BracketOrder
from google.protobuf.wrappers_pb2 import DoubleValue


trading_day = datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d')
# Create log directory
log_dir = os.path.join(os.getcwd(), r'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(threadName)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S%z',
    handlers=[
        logging.FileHandler(f'{log_dir}/EzeEMSxAPI_DayTrading_{trading_day}.log'),
        logging.StreamHandler()
    ]
)
logging.info('Logger initialized')

# Setup dotenv to store login credentials
env_file_path = os.path.join(os.getcwd(), '.env')
if not os.path.exists(env_file_path):
    open(env_file_path, 'w').close()
dotenv.load_dotenv()

#
# logFormatter = logging.Formatter(log_format)
# logger = logging.getLogger()
#
# fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
# fileHandler.setFormatter(logFormatter)
# logger.addHandler(fileHandler)
#
# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# logger.addHandler(consoleHandler)

# APIs:
# For getting all of today's orders:
#   GetTodaysActivity[Json]
#   GetTodaysNetPositions
#   GetTodaysBalances
#
# For getting stock prices:
#   SubscribeLevel1Ticks
#   GetLevel1MarketData
#   GetTickData
#
#


def print_info(obj, name=None):
    logging.info(f'Info for {f"{name}: " if name else ""}{str(obj)}')
    logging.info(f'Type: {type(obj)}')


def handle_data_example(response):
    try:
        for tick in response:
            if tick.Trdprc1.DecimalValue == 0.0:
                continue
            logging.info(f'Received market data for {tick.DispName}, Last traded price: {tick.Trdprc1.DecimalValue}')
    except Exception as e:
        logging.info(e)


def get_from_env_or_input(env_var_name, display_name, is_password=False):
    if os.getenv(env_var_name) is None:
        logging.info(f'No {display_name} found under env variable: {env_var_name}. Please input the {display_name} now')
        if is_password:
            value = getpass.getpass(f'{display_name}: ')
        else:
            value = input(f'{display_name}: ')
            logging.info(f'Received input: {value}')
        dotenv.set_key(env_file_path, env_var_name, value)

        logging.info(f'value: {value}, value type: {type(value)}')

        return value
    else:
        return os.getenv(env_var_name)


def login(util_stub, retry_count=5):
    user = get_from_env_or_input('EZE_EMS_USERNAME', 'Username')
    domain = get_from_env_or_input('EZE_EMS_DOMAIN', 'Domain')
    locale = get_from_env_or_input('EZE_EMS_LOCALE', 'Locale')
    password = get_from_env_or_input('EZE_EMS_PASSWORD', 'Password', is_password=True)

    for i in range(retry_count):
        logging.info(f'Attempting login for user: {user}, domain: {domain}, and locale: {locale}')
        connect_response = util_stub.Connect(util.ConnectRequest(UserName=user, Domain=domain, Password=password,
                                                                 Locale=locale))
        if connect_response.Response == 'success':
            logging.info(f'Successfully logged in, token={connect_response.UserToken} response='
                         f'{connect_response.Response}')
            return connect_response
        else:
            logging.info(f'Login attempt #{i + 1} failed: {connect_response}')
            if i == retry_count - 1:
                logging.info('All login attempts failed')
                raise Exception('Login failed!')
            else:
                delay_millis = 500 * 2**(i+1)  # Exponential delay for each retry
                logging.info(f'Retrying login after {delay_millis} milliseconds')
                time.sleep(delay_millis/1000)


# def get_order_id(order_tag, user_token):
#     activity_response = util_stub.GetTodaysActivityJson(
#         util.TodaysActivityJsonRequest(IncludeUserSubmitOrder=True, UserToken=user_token))
#     logging.info(f'activity_response type: {type(activity_response)}')
#     logging.info(f'activity_response str: {str(activity_response)}')
#     logging.info(f'activity_response: {activity_response}')
#     logging.info(f'activity_response.Acknowledgement: {activity_response.Acknowledgement}')
#     logging.info(f'activity_response.TodaysActivityJson: {activity_response.TodaysActivityJson}')
#     df = pd.read_json(activity_response.TodaysActivityJson, orient='records')
#     order_id = df.loc[df['OrderTag'] == order_tag]
#     for order in df:
#         logging.info(f'order type: {type(order)}')
#         logging.info(f'order str: {str(order)}')
#     logging.info(f'DF: \n{df}')
#     order_id = 'filler'
#     logging.info(f'Found order_id: {order_id} for tag: {order_tag}')
#     return order_id


def submit_order(ord_stub, symbol, side, quantity, route, account, order_tag, price_type, user_token, closing_order,
                 limit_price=None, stop_price=None):
    # Safeguard
    if symbol != 'ZVZZT':
        raise Exception('Calling order on non test stock: {}'.format(symbol))

    if price_type == 'Limit' or price_type == 'StopLimit':
        if not limit_price:
            logging.error(f'Submitting {price_type} trade without setting limit price')
    if price_type == 'StopMarket' or price_type == 'StopLimit':
        if not stop_price:
            logging.error(f'Submitting {price_type} trade without setting stop price')

    # Convert Limit and Stop prices to google.protobuf.DoubleValue
    limit_price = DoubleValue(value=limit_price) if limit_price else None
    stop_price = DoubleValue(value=stop_price) if stop_price else None

    order_request = ord.SubmitSingleOrderRequest(Symbol=symbol, Side=side, Quantity=quantity, Route=route,
                                                 Account=account, OrderTag=order_tag, UserToken=user_token,
                                                 Price=limit_price, StopPrice=stop_price, ReturnResult=True)
    # Extended field TO_OPEN_POS should be 100 for buy to open and sell short orders and 101 for buy to close and sell
    # long orders
    order_request.ExtendedFields['TO_OPEN_POS'] = '100' if not closing_order else '101'
    # Setting PriceType through the extended field rather than the SubmitSingleOrderRequest param because the param
    # asked for a PriceTypeEnum value, and I wasn't able to figure out how to give it that
    order_request.ExtendedFields['PRICE_TYPE'] = price_type
    # order_request.ExtendedFields['RETURN_RESULT'] = 'True'
    if side == 'SELLSHORT':
        # For SELLSHORT orders, extended field SHORT_LOCATE_ID must be assigned. Value can be anything
        order_request.ExtendedFields['SHORT_LOCATE_ID'] = order_tag
    logging.info(f'Submitting {side} {price_type} order (OrderTag={order_tag}) for {quantity} shares of {symbol}')
    # order_response = ord_stub.SubmitSingleOrder(order_request)
    retry_count = 5
    for i in range(retry_count):
        order_response = ord_stub.SubmitSingleOrder(order_request)
        if order_response.ServerResponse == 'success':
            return order_response
        else:
            logging.info(f'Order attempt #{i + 1} failed: {order_response}')
            if i == retry_count - 1:
                logging.info('All order attempts failed')
                return order_response
            else:
                delay_millis = 500 * 2**(i+1)  # Exponential delay for each retry
                logging.info(f'Retrying order after {delay_millis} milliseconds')
                time.sleep(delay_millis/1000)


def cancel_order(ord_stub, user_token, order_id):
    retry_count = 5
    for i in range(retry_count):
        cancel_response = ord_stub.CancelSingleOrder(
            ord.CancelSingleOrderRequest(OrderId=order_id, UserToken=user_token))
        if cancel_response.ServerResponse == 'success':
            return cancel_response
        else:
            logging.info(f'Cancel order attempt #{i + 1} failed: {cancel_response}')
            if i == retry_count - 1:
                logging.info('All cancel order attempts failed')
                return cancel_response
            else:
                delay_millis = 500 * 2 ** (i + 1)  # Exponential delay for each retry
                logging.info(f'Retrying cancel order after {delay_millis} milliseconds')
                time.sleep(delay_millis / 1000)


def get_order_status(ord_stub, user_token, order_id):
    retry_count = 5
    for i in range(retry_count):
        ord_response = ord_stub.GetOrderDetailByOrderIdJson(
            ord.OrderDetailByOrderIdJsonRequest(UserToken=user_token, OrderId=order_id))
        if ord_response.Acknowledgement.ServerResponse == 'success':
            return json.loads(ord_response.OrderDetail)[0]['CurrentStatus']
        else:
            logging.info(f'Get order details attempt #{i + 1} failed: {ord_response}')
            if i == retry_count - 1:
                logging.info('All Get order details attempts failed')
                return 'SERVICE CALL FAILED'
            else:
                delay_millis = 500 * 2 ** (i + 1)  # Exponential delay for each retry
                logging.info(f'Retrying Get order details after {delay_millis} milliseconds')
                time.sleep(delay_millis / 1000)


def get_current_stock_price(md_stub, user_token, symbol):
    retry_count = 5
    for i in range(retry_count):
        md_response = md_stub.GetLevel1MarketData(md.Level1MarketDataRequest(
            Symbols=[symbol], Request=True, UserToken=user_token))
        if md_response.Acknowledgement.ServerResponse == 'success':
            return True, md_response.DataRecord[0].Trdprc1.DecimalValue
        else:
            logging.info(f'Get market data attempt #{i + 1} failed: {md_response}')
            if i == retry_count - 1:
                logging.info('All Get market data attempts failed')
                return False, None
            else:
                delay_millis = 500 * 2 ** (i + 1)  # Exponential delay for each retry
                logging.info(f'Retrying Get market data after {delay_millis} milliseconds')
                time.sleep(delay_millis / 1000)


def moving_in_correct_direction(current_price, entry_price, direction):
    if direction == OrderDirection.LONG:
        return current_price < entry_price
    elif direction == OrderDirection.SHORT:
        return current_price > entry_price
    else:
        raise RuntimeError('No moving_in_correct_direction implementation for order direction: {}'.format(direction))


def adjust_entry_price(entry_price, direction):
    price_offset = 0.07  # Offset entry price by $0.07
    if direction == OrderDirection.LONG:
        return entry_price - price_offset
    elif direction == OrderDirection.SHORT:
        return entry_price + price_offset
    else:
        raise RuntimeError('No adjust_entry_price implementation for order direction: {}'.format(direction))


def at_or_better_than(current_price, compare_price, direction):
    if direction == OrderDirection.LONG:
        return current_price >= compare_price
    elif direction == OrderDirection.SHORT:
        return current_price <= compare_price
    else:
        raise RuntimeError('No at_or_better_than implementation for order direction: {}'.format(direction))


def at_or_worse_than(current_price, compare_price, direction):
    if direction == OrderDirection.LONG:
        return current_price <= compare_price
    elif direction == OrderDirection.SHORT:
        return current_price >= compare_price
    else:
        raise RuntimeError('No at_or_worse_than implementation for order direction: {}'.format(direction))


def handle_order(channel, user_token, order):
    try:
        entry_order_created = False
        entry_order_executed = False
        new_entry = None
        keep_going = True
        # Stubs
        md_stub = md_grpc.MarketDataServiceStub(channel)
        ord_stub = ord_grpc.SubmitOrderServiceStub(channel)
        # Time
        us_holidays = holidays.US()
        est_timezone = pytz.timezone('US/Eastern')

        logging.info(f'Starting processing for order: {order}')

        while keep_going:
            # If closing order has been entered, check if it has completed
            if order.closing_order_id:
                if get_order_status(ord_stub, user_token, order.closing_order_id) == 'COMPLETED':
                    logging.info(f'Closing order {order.closing_order_id} has completed for symbol {order.symbol}. '
                                 f'Finished all processing for this order')
                    break

            # Check time
            now_est = datetime.datetime.now(est_timezone)
            market_open = datetime.datetime(year=now_est.year, month=now_est.month, day=now_est.day, hour=9, minute=30,
                                            second=0, tzinfo=now_est.tzinfo)
            market_close = datetime.datetime(year=now_est.year, month=now_est.month, day=now_est.day, hour=16, minute=0,
                                             second=0, tzinfo=now_est.tzinfo)
            if now_est.strftime('%Y-%m-%d') in us_holidays:
                logging.info('Today is a holiday so markets are closed')
                break
            elif now_est.date().weekday() > 4:
                logging.info('It is the weekend so markets are closed')
                break
            elif not (market_open <= now_est < market_close):
                logging.info(f'Market is not open at this time ({now_est.strftime("%Y-%m-%d %H:%M:%S %Z")})')
                if now_est < market_open:
                    seconds_til_open = (market_open - now_est).total_seconds()
                    logging.info(f'Waiting {seconds_til_open} seconds for market to open...')
                    time.sleep(seconds_til_open)
                    continue
                else:
                    logging.info('Market has closed for the day. Try again tomorrow')
                    break
            elif now_est.time() > datetime.time(hour=15, minute=30, second=0) and not entry_order_executed:
                logging.info('Reached 3pm EST without entry order executing')
                if entry_order_created:
                    # Cancel entry order
                    logging.info(f'Cancelling entry order: {order.order_id}')
                    cancel_response = cancel_order(ord_stub=ord_stub, user_token=user_token, order_id=order.order_id)
                    logging.info(f'Cancel order response: {cancel_response}')
                    if cancel_response.ServerResponse == 'success':
                        logging.info(f'Successfully cancelled order: {order.order_id}. Exiting')
                    else:
                        logging.warning(f'Failed to cancel order: {order.order_id}. Please address')
                else:
                    logging.info('Entry order has not been submitted. Exiting')
                break
            elif now_est.time() > datetime.time(hour=15, minute=50, second=0):
                logging.info('Reached 3:50pm ET and the entry order has been executed but potentially not closed out')
                # Check for any open orders
                if order.closing_order_id:
                    closing_order_status = get_order_status(ord_stub, user_token, order.closing_order_id)
                    if closing_order_status != 'COMPLETED':
                        logging.info(f'Cancelling order {order.closing_order_id} as it is 3:50pm and it is in status: '
                                     f'{closing_order_status}')
                        cancel_response = cancel_order(ord_stub=ord_stub, user_token=user_token,
                                                       order_id=order.closing_order_id)
                        if cancel_response.ServerResponse == 'success':
                            logging.info(f'Successfully cancelled order: {order.closing_order_id}')
                        else:
                            logging.warning(f'Failed to cancel order: {order.closing_order_id}. Please address')
                    else:
                        # Closing order has completed so no further orders are needed
                        break
                side = 'SELL' if order.direction == OrderDirection.LONG else 'BUY'
                price_type = 'Market'
                logging.info(f'3:50pm reached and order for {order.symbol} has not closed out yet. Sending {side} '
                             f'{price_type} order to close out.')
                order.closing_order_tag = str(uuid.uuid4())
                order_response = submit_order(
                    ord_stub=ord_stub, symbol=order.symbol, side=side, quantity=order.quantity, route=order.route,
                    account=order.account, order_tag=order.closing_order_tag, price_type=price_type,
                    user_token=user_token, closing_order=True)
                logging.info(f'Closing order result: {order_response}')
                if order_response.ServerResponse != 'success':
                    logging.warning('Order failed to submit')
                else:
                    order.closing_order_id = order_response.OrderDetails.OrderId

            # If entry order is entered but not executed: wait
            if entry_order_created and not entry_order_executed:
                # Check on order status
                if get_order_status(ord_stub, user_token, order.order_id) == 'COMPLETED':
                    entry_order_executed = True
                else:
                    time.sleep(3)
            else:
                # Get current market data for symbol
                success, current_price = get_current_stock_price(md_stub, user_token, order.symbol)
                if not success:
                    logging.warning(f'Failed to get current stock price for symbol [{order.symbol}]. Waiting 5 seconds '
                                    f'before retrying...')
                    time.sleep(5)
                    continue

                # If no entry order created yet: Check stock price. If it's moving in the correct direction in relation
                # to the entry price (below entry if LONG and above entry if SHORT), enter Stop entry order
                if not entry_order_created:
                    entry_price = new_entry if new_entry is not None else order.entry_price
                    if moving_in_correct_direction(current_price, entry_price, order.direction):
                        side = 'BUY' if order.direction == OrderDirection.LONG else 'SELLSHORT'
                        price_type = 'StopLimit' if order.entry_limit else 'StopMarket'
                        logging.info(f'Submitting {side} {price_type} entry order for {order.symbol}')
                        order.order_tag = str(uuid.uuid4())
                        order_response = submit_order(
                            ord_stub=ord_stub, symbol=order.symbol, side=side, quantity=order.quantity,
                            route=order.route, account=order.account, order_tag=order.order_tag, price_type=price_type,
                            user_token=user_token, closing_order=False, limit_price=order.entry_limit,
                            stop_price=order.entry_price)
                        logging.info(f'Order result: {order_response}')
                        if order_response.ServerResponse != 'success':
                            logging.warning('Entry order failed to submit')
                        else:
                            order.order_id = order_response.OrderDetails.OrderId
                            entry_order_created = True
                    elif new_entry is None:
                        new_entry = adjust_entry_price(order.entry_price, order.direction)
                        logging.info(f'Current price for {order.symbol} is {current_price} and entry price is '
                                     f'{order.entry_price}, which is moving in the wrong direction for a '
                                     f'{order.direction} trade so we adjust entry to be {new_entry}')
                # If entry order is entered and executed:
                else:
                    # If price is target or better: enter limit trade to close out
                    if at_or_better_than(current_price, order.target_price, order.direction):
                        side = 'SELL' if order.direction == OrderDirection.LONG else 'BUY'
                        price_type = 'Limit'
                        logging.info(f'Target price of {order.target_price} reached for {order.symbol}. Sending {side}'
                                     f'{price_type} order to close out.')
                        order.closing_order_tag = str(uuid.uuid4())
                        order_response = submit_order(
                            ord_stub=ord_stub, symbol=order.symbol, side=side, quantity=order.quantity,
                            route=order.route, account=order.account, order_tag=order.closing_order_tag,
                            price_type=price_type, user_token=user_token, closing_order=True,
                            limit_price=order.target_price)
                        logging.info(f'Closing order result: {order_response}')
                        if order_response.ServerResponse != 'success':
                            logging.warning('Order failed to submit')
                        else:
                            order.closing_order_id = order_response.OrderDetails.OrderId
                    # If price is $0.10 or better: Change stop-loss price to 50%
                    elif at_or_better_than(current_price, order.near_target, order.direction) \
                            and not at_or_better_than(order.stop_loss_price, order.half_target, order.direction):
                        logging.info(f'{order.symbol} has reached near_target price of {order.near_target}. Setting '
                                     f'stop_loss_price to {order.half_target}')
                        order.stop_loss_price = order.half_target
                    # If price is 50% or better: Change stop-loss price to entry price
                    elif at_or_better_than(current_price, order.half_target, order.direction) \
                            and not at_or_better_than(order.stop_loss_price, order.entry_price, order.direction):
                        logging.info(f'{order.symbol} has reached half_target price of {order.half_target}. Setting '
                                     f'stop_loss_price to {order.entry_price}')
                        order.stop_loss_price = order.entry_price
                    # If price is stop-loss or worse: Enter market or limit order to close out
                    elif at_or_worse_than(current_price, order.stop_loss_price, order.direction):
                        logging.info(f'Stop-loss price of {order.stop_loss_price} reached for {order.symbol}')
                        # First check if there is an open closing order already. This can occur if target price was
                        # reached and a limit order was sent to close out at target, and then the price kept falling and
                        # the trade was never executed
                        if order.closing_order_id:
                            logging.info(f'Cancelling unexecuted closing order (OrderId={order.closing_order_id}) for '
                                         f'{order.symbol}')
                            cancel_response = cancel_order(ord_stub=ord_stub, user_token=user_token,
                                                           order_id=order.closing_order_id)
                            if cancel_response.ServerResponse == 'success':
                                logging.info(f'Successfully cancelled order: {order.closing_order_id}')
                            else:
                                logging.warning(f'Failed to cancel order: {order.closing_order_id}. Please address')
                        side = 'SELL' if order.direction == OrderDirection.LONG else 'BUY'
                        price_type = 'Limit' if order.stop_loss_order_type == OrderType.LIMIT else 'Market'
                        limit_price = order.stop_loss_price if order.stop_loss_order_type == OrderType.LIMIT else None
                        logging.info(f'Stop-loss price of {order.stop_loss_price} reached for {order.symbol}. Sending '
                                     f'{side} {price_type} order to close out')
                        order.closing_order_tag = str(uuid.uuid4())
                        order_response = submit_order(
                            ord_stub=ord_stub, symbol=order.symbol, side=side, quantity=order.quantity,
                            route=order.route, account=order.account, order_tag=order.closing_order_tag,
                            price_type=price_type, user_token=user_token, closing_order=True, limit_price=limit_price)
                        logging.info(f'Closing order result: {order_response}')
                        if order_response.ServerResponse != 'success':
                            logging.warning('Order failed to submit')
                        else:
                            order.closing_order_id = order_response.OrderDetails.OrderId
    except Exception as e:
        logging.exception(f'Exception occurred: {e}')


if __name__ == '__main__':
    # Read in file
    # load each trade into an array of BracketOrders
    orders = []
    orders.append(BracketOrder(route='NSDQ-LS', account='LSPS;01;LSPS;1LD51021', symbol='ZVZZT', quantity=3,
                               direction=OrderDirection.LONG, entry_price=15, stop_loss_price=12, target_price=19,
                               entry_order_type=OrderType.MARKET, entry_limit=None, half_target=17, near_target=18.50))

    with open(r'.\roots.pem', 'rb') as f:
        cert = f.read()
    server = 'chixapi.taltrade.com'
    port = '9000'
    channel = grpc.secure_channel('{}:{}'.format(server, port), grpc.ssl_channel_credentials(root_certificates=cert))
    logging.info(f'Channel: {channel}')
    util_stub = util_grpc.UtilityServicesStub(channel)

    connect_response = None
    try:
        # for e in OrderType:
        #     logging.info(f'OrderType: {e}')
        #     logging.info(f'OrderType: {type(e)}')

        # pt = util.PriceTypeEnum.PriceTypesEnum.StopMarket
        # print_info(pt)
        # pt2 = util.PriceTypeEnum.PriceTypesEnum.Other
        # print_info(pt2)
        # pt3 = util.PriceTypeEnum.StopMarket
        # print_info(pt3)
        # pt4 = util.PriceTypeEnum
        # print_info(pt4)
        # pt5 = util.PriceTypeEnum.PriceTypesEnum.values()
        # print_info(pt5)
        # pt6 = util.PriceTypeEnum.PriceTypesEnum.keys()
        # print_info(pt6)
        # logging.info(f'dir: {dir(util.PriceTypeEnum)}')

        # logging.info(f'SubmitSingleOrderRequest dir: {dir(ord.SubmitSingleOrderRequest)}')
        # logging.info(f'SubmitSingleOrderRequest ListFields: {ord.SubmitSingleOrderRequest.ListFields()}')
        #

        connect_response = login(util_stub=util_stub)
        # logging.info('Exiting early')
        # exit(0)

        # ord_stub = ord_grpc.SubmitOrderServiceStub(channel)
        # orders[0].order_tag = str(uuid.uuid4())
        # price_type = 'Limit'
        # my_limit_price = 12.00
        # my_order_response = submit_order(
        #     ord_stub=ord_stub, symbol=orders[0].symbol, side='BUY', quantity=orders[0].quantity, route=orders[0].route,
        #     account=orders[0].account, order_tag=orders[0].order_tag, price_type=price_type,
        #     user_token=connect_response.UserToken, closing_order=False, limit_price=my_limit_price)
        # # get_order_id('88077341-11d1-471e-a1c5-31bf7520bfe3', connect_response.UserToken)
        # # get_order_id('24b28c2a-4295-4749-bdc4-8e1e3b585ebf', connect_response.UserToken)
        # logging.info(f'Order response type: {type(my_order_response)}')
        # logging.info(f'Order response string: {str(my_order_response)}')
        # logging.info(f'Order response dir: {dir(my_order_response)}')
        # logging.info(f'Order response SerializeToString: {str(my_order_response.SerializeToString())}')
        # logging.info(f'Order response ListFields: {str(my_order_response.ListFields())}')
        # logging.info(f'Order response [OrderDetails]: {str(my_order_response.OrderDetails)}')
        # logging.info(f'Order response dir [OrderDetails]: {dir(my_order_response.OrderDetails)}')
        # logging.info(f'Order response type [OrderDetails]: {type(my_order_response.OrderDetails)}')
        # logging.info(f'Order response OrderId [OrderDetails]: {my_order_response.OrderDetails.OrderId}')

        threads = [Thread(target=handle_order, args=(channel, connect_response.UserToken, order)) for order in orders]
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
        logging.info(f'Finished run for {trading_day}')
    except Exception as e:
        logging.exception(f'Exception occurred of type: {type(e).__name__} with args: {e.args}')
    finally:
        if connect_response and connect_response.Response == 'success':
            disconnect_response = util_stub.Disconnect(util.DisconnectRequest(UserToken=connect_response.UserToken))
            logging.info(f'Disconnect result: {disconnect_response.ServerResponse}')
