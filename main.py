import json
import threading

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

# Initialize lock
lock = threading.Lock()


def print_info(obj, name):
    logging.info(f'{name}      - {obj}')
    logging.info(f'{name} type - {type(obj)}')
    logging.info(f'{name} dir  - {dir(obj)}')


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
        connect_response_local = util_stub.Connect(util.ConnectRequest(UserName=user, Domain=domain, Password=password,
                                                                       Locale=locale))
        if connect_response_local.Response == 'success':
            logging.info(f'Successfully logged in, token={connect_response_local.UserToken} response='
                         f'{connect_response_local.Response}')
            return connect_response_local
        else:
            logging.info(f'Login attempt #{i + 1} failed: {connect_response_local}')
            if i == retry_count - 1:
                logging.info('All login attempts failed')
                raise Exception('Login failed!')
            else:
                delay_millis = 500 * 2**(i+1)  # Exponential delay for each retry
                logging.info(f'Retrying login after {delay_millis} milliseconds')
                time.sleep(delay_millis/1000)


def get_order_id(util_stub, user_token, order_tag):
    with lock:
        activity_response = util_stub.GetTodaysActivityJson(
            util.TodaysActivityJsonRequest(IncludeUserSubmitOrder=True, UserToken=user_token))
    logging.info(f'activity_response type: {type(activity_response)}')
    logging.info(f'activity_response str: {str(activity_response)}')
    logging.info(f'activity_response: {activity_response}')
    logging.info(f'activity_response.Acknowledgement: {activity_response.Acknowledgement}')
    logging.info(f'activity_response.TodaysActivityJson: {activity_response.TodaysActivityJson}')
    df = pd.read_json(activity_response.TodaysActivityJson, orient='records')
    order_id = df.loc[df['OrderTag'] == order_tag]
    for order in df:
        logging.info(f'order type: {type(order)}')
        logging.info(f'order str: {str(order)}')
    logging.info(f'DF: \n{df}')
    order_id = 'filler'
    logging.info(f'Found order_id: {order_id} for tag: {order_tag}')
    return order_id


def get_order_details(util_stub, request, order_tag, retry_count=5) -> (bool, dict):
    """
    Gets orders placed today that match the given order_tag
    :return: List of order details for all orders matching the given order_tag
    """
    for i in range(retry_count):
        with lock:
            activity_response = util_stub.GetTodaysActivityJson(request)
        if activity_response.Acknowledgement.ServerResponse == 'success':
            activity_df = pd.read_json(activity_response.TodaysActivityJson, orient='records')
            orders_by_tag = activity_df.loc[activity_df['OrderTag'] == order_tag]
            order_details = orders_by_tag.to_dict('records')
            if len(order_details) > 1:
                logging.error(f'CRITICAL ERROR: Multiple ({len(order_details)}) user submitted orders found with order '
                              f'tag [{order_tag}]. Orders are:\n{order_details}\nExiting thread. Please address '
                              f'duplicate orders manually.')
                exit(1)
            elif len(order_details) < 1:
                # logging.warning(f'Found no orders with order tag [{order_tag}]')
                return True, None
            else:
                # Sanity check to make sure server is returning valid objects
                if order_details[0]['CurrentStatus'] is None:
                    logging.error(f'Received empty OrderDetails object from server for OrderTag={order_tag}. Full '
                                  f'response: {activity_response}')
                return True, order_details[0]
        else:
            logging.info(f'get_order_details_by_order_tag attempt #{i + 1} failed: {activity_response}')
            if i == retry_count - 1:
                logging.info('All get_order_details_by_order_tag attempts failed')
                return False, activity_response
            else:
                delay_millis = 500 * 2 ** (i + 1)  # Exponential delay for each retry
                logging.info(f'Retrying get_order_details_by_order_tag after {delay_millis} milliseconds')
                time.sleep(delay_millis / 1000)


def get_user_submit_order_details(util_stub, user_token, order_tag) -> (bool, dict):
    """
    Gets all user submitted orders placed today that match the given order_tag
    :return: List of order details for all orders matching the given order_tag
    """
    return get_order_details(
        util_stub, util.TodaysActivityJsonRequest(IncludeUserSubmitOrder=True, UserToken=user_token), order_tag)


def get_exchange_trade_order_details(util_stub, user_token, order_tag) -> (bool, dict):
    """
    Gets all exchange trade order details from today that match the given order_tag
    :return: List of order details for all orders matching the given order_tag
    """
    return get_order_details(
        util_stub, util.TodaysActivityJsonRequest(IncludeExchangeTradeOrder=True, UserToken=user_token), order_tag)


def submit_order(ord_stub, util_stub, symbol, side, quantity, route, account, order_tag, price_type, user_token,
                 closing_order, limit_price=None, stop_price=None, retry_count=5) -> (bool, dict):

    # todo dont even make the call if it has invalid params
    if price_type == 'Limit' or price_type == 'StopLimit':
        if not limit_price:
            logging.error(f'Submitting {price_type} trade without setting limit price')
    if price_type == 'StopMarket' or price_type == 'StopLimit':
        if not stop_price:
            logging.error(f'Submitting {price_type} trade without setting stop price')

    price_type_enum = util.PriceTypeEnum()
    price_type_enum.PriceType = util.PriceTypeEnum.PriceTypesEnum.Value(price_type)

    # Convert Limit and Stop prices to google.protobuf.DoubleValue
    limit_price = DoubleValue(value=limit_price) if limit_price else None
    stop_price = DoubleValue(value=stop_price) if stop_price else None

    # ReturnResult is a parameter that tells the server to return the submitted order details in the response. However,
    # in testing this input seemed to be buggy, either causing a timeout ('Timed out waiting for Streaming Event'), or
    # returning the details of a different order than the one that was submitted. Setting this to false for now but in
    # the future if this is fixed it would more convenient way of getting order ID than making a separate service call
    return_result = True

    # logging.info(f'Stop price: {stop_price}')
    # logging.info(f'Stop price type: {type(stop_price)}')
    order_request = ord.SubmitSingleOrderRequest(Symbol=symbol, Side=side, Quantity=quantity, Route=route,
                                                 Account=account, OrderTag=order_tag, UserToken=user_token,
                                                 Price=limit_price, StopPrice=stop_price, ReturnResult=return_result,
                                                 PriceType=price_type_enum)
    # Extended field TO_OPEN_POS should be 100 for buy to open and sell short orders and 101 for buy to close and sell
    # long orders
    order_request.ExtendedFields['TO_OPEN_POS'] = '100' if not closing_order else '101'
    # Setting PriceType through the extended field rather than the SubmitSingleOrderRequest param because the param
    # asked for a PriceTypeEnum value, and I wasn't able to figure out how to give it that
    # order_request.ExtendedFields['PRICE_TYPE'] = price_type
    # order_request.ExtendedFields['RETURN_RESULT'] = 'True'
    if side == 'SELLSHORT':
        # For SELLSHORT orders, extended field SHORT_LOCATE_ID must be assigned. Value can be anything
        order_request.ExtendedFields['SHORT_LOCATE_ID'] = order_tag
    logging.info(f'Submitting {side} {price_type} order (OrderTag={order_tag}) for {quantity} shares of {symbol}')
    # order_response = ord_stub.SubmitSingleOrder(order_request)
    for i in range(retry_count):
        with lock:
            logging.info(f'lock acquired')
            logging.info(f'order_request: {order_request}')
            submit_order_response = ord_stub.SubmitSingleOrder(order_request)
            logging.info(f'submit_order_response for symbol [{symbol}]: {submit_order_response}')
            logging.info(f'releasing lock...')

        # if submit_order_response.ServerResponse == 'success':
        #     return True, submit_order_response
        # else:
        #     logging.warning(f'SubmitOrder attempt #{i + 1} failed: {submit_order_response}')
        #     if i == retry_count - 1:
        #         logging.info('All SubmitOrder attempts failed')
        #         return False, submit_order_response
        #     else:
        #         delay_millis = 500 * 2 ** (i + 1)  # Exponential delay for each retry
        #         logging.info(f'Retrying SubmitOrder after {delay_millis} milliseconds...')
        #         time.sleep(delay_millis / 1000)
        #         logging.info(f'Retrying SubmitOrder (OrderTag={order_tag}) now')

        # Now query the server for order details, retrying after a delay if no order is found to give the system time
        # to propagate the order
        for j in range(retry_count):
            success, details = get_user_submit_order_details(util_stub, user_token, order_tag)
            if success:
                if details is not None:
                    if submit_order_response.ServerResponse == 'success':
                        logging.info(
                            f'Successfully submitted order with tag [{order_tag}] and ID [{details["OrderId"]}]')
                    else:
                        logging.warning(f'Submit order call failed however an order with tag [{order_tag}] and ID '
                                        f'[{details["OrderId"]}] was found. Order response: {submit_order_response}')
                    return True, details
                else:
                    logging.warning(f'Found no order details for tag [{order_tag}]. This was attempt #{j + 1}')
                    if j == retry_count - 1:
                        logging.info(f'All GetOrderDetails attempts returned empty for tag [{order_tag}]')
                        if submit_order_response.ServerResponse == 'success':
                            logging.warning(
                                f'Submit order call succeeded but no order was found with tag [{order_tag}]. '
                                f'SubmitOrder response: {submit_order_response}.')
                            return True, None
                        else:
                            logging.warning(f'Order [OrderTag={order_tag}] failed to submit. SubmitOrder response: '
                                            f'{submit_order_response}')
                            return False, submit_order_response
                    else:
                        delay_millis = 500 * 2 ** (j + 1)  # Exponential delay for each retry
                        logging.info(f'Retrying GetOrderDetails after {delay_millis} milliseconds...')
                        time.sleep(delay_millis / 1000)
                        logging.info(f'Retrying GetOrderDetails (OrderTag={order_tag}) now')

            else:
                logging.warning(f'GetOrderDetails failed with response: {details}')
                if submit_order_response.ServerResponse == 'success':
                    logging.warning(f'GetOrderDetails failed but SubmitOrder [tag={order_tag}] succeeded with response:'
                                    f' {submit_order_response}')
                    return True, None
                else:
                    logging.warning(f'Failed to submit order [{order_tag}]')
                    return False, submit_order_response


# def submit_order_and_get_details(ord_stub, util_stub, symbol, side, quantity, route, account, order_tag, price_type,
#                                  user_token, closing_order, limit_price=None, stop_price=None) -> (bool, dict):
#     """
#     Helper method to retry get_order_details with delays in case no order is found but the submit order call succeeds
#     :return:
#     """
#     success, response = submit_order(ord_stub, util_stub, symbol, side, quantity, route, account, order_tag, price_type,
#                                      user_token, closing_order, limit_price, stop_price)
#
#     success, details = get_order_details_by_order_tag(util_stub, user_token, order_tag)


def cancel_order(ord_stub, user_token, order_id):
    retry_count = 5
    for i in range(retry_count):
        with lock:
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
        with lock:
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


# def get_order_details(ord_stub, user_token, order_id) -> (bool, dict):
#     retry_count = 5
#     for i in range(retry_count):
#         with lock:
#             ord_response = ord_stub.GetOrderDetailByOrderIdJson(
#                 ord.OrderDetailByOrderIdJsonRequest(UserToken=user_token, OrderId=order_id))
#         if ord_response.Acknowledgement.ServerResponse == 'success':
#             if json.loads(ord_response.OrderDetail)[0]['CurrentStatus'] is None:
#                 logging.warning(f'Received empty OrderDetails object from server for OrderId={order_id}. Full '
#                                 f'response: {ord_response}')
#             else:
#                 if len(json.loads(ord_response.OrderDetail)) > 1:
#                     logging.error(f'Found more than one order for order ID [{order_id}]: {len(json.loads(ord_response.OrderDetail))}\n '
#                                   f'Orders: {json.loads(ord_response.OrderDetail)}')
#                 return True, json.loads(ord_response.OrderDetail)[0]
#         logging.info(f'Get order details attempt #{i + 1} failed: {ord_response}')
#         if i == retry_count - 1:
#             logging.info('All Get order details attempts failed')
#             return False, None
#         else:
#             delay_millis = 500 * 2 ** (i + 1)  # Exponential delay for each retry
#             logging.info(f'Retrying Get order details after {delay_millis} milliseconds')
#             time.sleep(delay_millis / 1000)


def get_current_stock_price(md_stub, user_token, symbol, retry_count=5) -> (bool, float):
    for i in range(retry_count):
        with lock:
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
        raise RuntimeError(f'No moving_in_correct_direction implementation for order direction: {direction}')


def adjust_entry_price(entry_price, direction):
    price_offset = 0.07  # Offset entry price by $0.07
    if direction == OrderDirection.LONG:
        return entry_price - price_offset
    elif direction == OrderDirection.SHORT:
        return entry_price + price_offset
    else:
        raise RuntimeError(f'No adjust_entry_price implementation for order direction: {direction}')


def at_or_better_than(current_price, compare_price, direction):
    if direction == OrderDirection.LONG:
        return current_price >= compare_price
    elif direction == OrderDirection.SHORT:
        return current_price <= compare_price
    else:
        raise RuntimeError(f'No at_or_better_than implementation for order direction: {direction}')


def at_or_worse_than(current_price, compare_price, direction):
    if direction == OrderDirection.LONG:
        return current_price <= compare_price
    elif direction == OrderDirection.SHORT:
        return current_price >= compare_price
    else:
        raise RuntimeError(f'No at_or_worse_than implementation for order direction: {direction}')


def log_heartbeat(md_stub, util_stub, user_token, order, entry_order_executed):
    heartbeat_string = f'Heartbeat for symbol [{order.symbol}]:\n'
    # Get current market data for symbol
    success, current_price = get_current_stock_price(md_stub, user_token, order.symbol)
    if success:
        heartbeat_string += f'Last traded price for {order.symbol}: {current_price}\n'
    else:
        heartbeat_string += f'Failed to get last traded price for {order.symbol}\n'
        logging.warning(f'Failed to get current stock price for symbol [{order.symbol}] while generating '
                        f'heartbeat')
    if order.order_tag:
        heartbeat_string += \
            f'Entry order has been submitted {"and" if entry_order_executed else "but not"} executed ' \
            f'with order ID: {order.order_id}\n'
        if entry_order_executed:
            success, entry_order_details = get_exchange_trade_order_details(util_stub, user_token,
                                                                            order.order_tag)
        else:
            success, entry_order_details = get_user_submit_order_details(util_stub, user_token,
                                                                         order.order_tag)
        if success:
            heartbeat_string += f'Entry order details: {entry_order_details}\n'
        else:
            heartbeat_string += f'Failed to get entry order details\n'
            logging.warning(f'Failed to get entry_order_details for symbol [{order.symbol}] while '
                            f'generating heartbeat. Response: {entry_order_details}')
    else:
        heartbeat_string += 'Entry order has not been submitted yet\n'
    if order.closing_order_tag:
        success, closing_order_details = get_user_submit_order_details(util_stub, user_token,
                                                                       order.closing_order_tag)
        heartbeat_string += f'Closing order has been submitted with order ID: {order.closing_order_id}\n'
        if success:
            heartbeat_string += f'Closing order details: {closing_order_details}\n'
        else:
            heartbeat_string += f'Failed to get closing order details\n'
            logging.warning(f'Failed to get closing_order_details for symbol [{order.symbol}] while '
                            f'generating heartbeat. Response: {closing_order_details}')
    else:
        heartbeat_string += f'Closing order has not been submitted yet\n'
    heartbeat_string += f'Order object: {order}\n'  # Todo: remove when testing is done as this isn't important to user
    logging.info(heartbeat_string)


def order_sanity_check(order):
    comparison_str = 'less than' if order.direction == OrderDirection.LONG else 'greater than'
    if (order.direction == OrderDirection.LONG and not order.stop_loss_price < order.entry_price < order.half_target < order.near_target < order.target_price) or \
            (order.direction == OrderDirection.SHORT and not order.stop_loss_price > order.entry_price > order.half_target > order.near_target > order.target_price):
        logging.error(
            f'{order.direction} order for [{order.symbol}] has invalid prices: stop_loss_price '
            f'[{order.stop_loss_price}] should be {comparison_str} entry_price [{order.entry_price}] which should be '
            f'{comparison_str} half_target [{order.half_target}] which should be {comparison_str} near_target '
            f'[{order.near_target}] which should be {comparison_str} target_price [{order.target_price}]')
        raise RuntimeError(f'Prices for [{order.symbol}] order are invalid. Order details: {order}')
    if order.entry_limit and ((order.direction == OrderDirection.LONG and not order.entry_price < order.entry_limit) or
                              (order.direction == OrderDirection.SHORT and not order.entry_price > order.entry_limit)):
        logging.error(f'{order.direction} order for [{order.symbol}] has invalid entry limit price: entry_price '
                      f'[{order.entry_price}] should be {comparison_str} entry_limit [{order.entry_limit}]')
        raise RuntimeError(f'Entry price for [{order.symbol}] order is invalid. Order details: {order}')
    if order.direction not in [OrderDirection.LONG, OrderDirection.SHORT]:
        raise RuntimeError(f'No order_sanity_check implementation for order direction: {order.direction}')


def handle_order(channel, user_token, order):
    try:
        # Change thread name to include stock symbol
        threading.current_thread().name = f'Thread-{order.symbol}'

        # Sanity check to make sure orders have prices setup correctly
        order_sanity_check(order)

        entry_order_executed = False
        stop_loss_order_submitted = False
        new_entry = None
        keep_going = True
        # Stubs
        md_stub = md_grpc.MarketDataServiceStub(channel)
        ord_stub = ord_grpc.SubmitOrderServiceStub(channel)
        util_stub = util_grpc.UtilityServicesStub(channel)
        # Time
        us_holidays = holidays.US()
        est_timezone = pytz.timezone('US/Eastern')
        # Heartbeat timer
        last_heartbeat = None

        logging.info(f'Starting processing for order: {order}')

        while keep_going:
            now_est = datetime.datetime.now(est_timezone)

            # Log heartbeat every X minutes giving update on current status
            if last_heartbeat is None or now_est >= last_heartbeat + datetime.timedelta(minutes=5):
                log_heartbeat(md_stub, util_stub, user_token, order, entry_order_executed)
                last_heartbeat = now_est

            # Safety check todo implement to check for multiple open entry or closing orders. Consider putting before submit_order call so api calls are limited
            # check_for_errors()

            # If closing order has been entered, check if it has completed
            if order.closing_order_tag:
                success, closing_order_details = get_user_submit_order_details(util_stub, user_token,
                                                                               order.closing_order_tag)
                if not success:
                    logging.warning(f'Failed to get closing_order_details for symbol [{order.symbol}]. Waiting 5 '
                                    f'seconds before retrying...')
                    time.sleep(5)
                elif closing_order_details['CurrentStatus'].upper() == 'COMPLETED':
                    logging.info(f'Closing order {order.closing_order_id} has completed for symbol {order.symbol}. '
                                 f'Finished all processing for this order. Exiting...')
                    break

            # Check time
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
                    logging.info('Market has closed for the day. Try again tomorrow...')
                    break
            elif now_est.time() > datetime.time(hour=15, minute=40, second=0) and not entry_order_executed: # Fixme rest to 3pm
                logging.info('Reached 3pm EST without entry order executing')
                if order.order_tag:
                    # Cancel entry order
                    logging.info(f'Cancelling entry order: {order.order_id}')
                    cancel_response = cancel_order(ord_stub=ord_stub, user_token=user_token, order_id=order.order_id)
                    logging.info(f'Cancel order response: {cancel_response}')
                    if cancel_response.ServerResponse == 'success':
                        logging.info(f'Successfully cancelled order: {order.order_id}. Exiting')
                    else:
                        logging.warning(f'Failed to cancel order: {order.order_id}. Please address manually!')
                else:
                    logging.info('Entry order has not been submitted. Exiting...')
                break
            elif now_est.time() > datetime.time(hour=15, minute=50, second=0):
                logging.info('Reached 3:50pm ET and the entry order has been executed but potentially not closed out')
                # Check for any open orders
                if order.closing_order_tag:
                    success, closing_order_details = get_user_submit_order_details(util_stub, user_token,
                                                                                   order.closing_order_tag)
                    if success:
                        if closing_order_details['CurrentStatus'].upper() != 'COMPLETED':
                            logging.info(f'Cancelling closing order [{order.closing_order_id}] as it is 3:50pm and it '
                                         f'is in status: {closing_order_details["CurrentStatus"]}')
                        else:
                            # Closing order has completed so no further orders are needed
                            logging.info(f'Closing order has executed (details={closing_order_details})\nEnding '
                                         f'processing for symbol: {order.symbol}...')
                            break
                    else:
                        logging.info(f'Failed to get closing order details. Server response: {closing_order_details}')
                    # Try to cancel the order as it has potentially not completed
                    cancel_response = cancel_order(ord_stub=ord_stub, user_token=user_token,
                                                   order_id=order.closing_order_id)
                    if cancel_response.ServerResponse == 'success':
                        logging.info(f'Successfully cancelled order: {order.closing_order_id}')
                        order.closing_order_tag = None
                    else:
                        logging.warning(f'Failed to cancel order: {order.closing_order_id}. Please address manually!')
                side = 'SELL' if order.direction == OrderDirection.LONG else 'BUY'
                price_type = 'Market'
                logging.info(f'3:50pm reached and order for {order.symbol} has not closed out yet. Sending {side} '
                             f'{price_type} order to close out.')
                order.closing_order_tag = str(uuid.uuid4())
                success, order_response = submit_order(
                    ord_stub=ord_stub, util_stub=util_stub, symbol=order.symbol, side=side, quantity=order.quantity,
                    route=order.route, account=order.account, order_tag=order.closing_order_tag, price_type=price_type,
                    user_token=user_token, closing_order=True, retry_count=7)
                if success:
                    logging.info(f'EOD closing order successfully submitted. Order details: {order_response}. Since '
                                 f'this is the final trade to make for the day, processing for {order.symbol} is done. '
                                 f'Exiting...')
                else:
                    logging.warning(f'EOD closing order failed to submit with order response: {order_response}. '
                                    f'Please address manually! Exiting...')
                break

            # If entry order is entered but not executed: wait
            if order.order_tag and not entry_order_executed:
                success, entry_order_details = get_user_submit_order_details(util_stub, user_token, order.order_tag)
                if not success:
                    logging.warning(f'Failed to get entry_order_details for symbol [{order.symbol}]. Waiting 5 '
                                    f'seconds before retrying...')
                    time.sleep(5)
                # Check on order status
                elif entry_order_details['CurrentStatus'].upper() == 'COMPLETED':
                    entry_order_executed = True
                    logging.info(f'Entry order has executed for [{order.symbol}]. Order details: {entry_order_details}')
                else:
                    # Wait a bit between API calls
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
                if not order.order_tag:
                    entry_price = new_entry if new_entry is not None else order.entry_price
                    if moving_in_correct_direction(current_price, entry_price, order.direction):
                        side = 'BUY' if order.direction == OrderDirection.LONG else 'SELLSHORT'
                        price_type = 'StopLimit' if order.entry_limit else 'StopMarket'
                        logging.info(f'Submitting {side} {price_type} entry order for {order.symbol}')
                        order.order_tag = str(uuid.uuid4())
                        success, order_response = submit_order(
                            ord_stub=ord_stub, util_stub=util_stub, symbol=order.symbol, side=side, quantity=order.quantity,
                            route=order.route, account=order.account, order_tag=order.order_tag, price_type=price_type,
                            user_token=user_token, closing_order=False, limit_price=order.entry_limit,
                            stop_price=order.entry_price)
                        if success:
                            logging.info(f'Entry order successfully submitted with order details: {order_response}')
                            if order_response:
                                order.order_id = order_response['OrderId']
                        else:
                            logging.warning(f'Entry order failed to submit. Order response: {order_response}')
                            order.order_tag = None
                    elif new_entry is None:
                        new_entry = adjust_entry_price(order.entry_price, order.direction)
                        logging.info(f'Current price for {order.symbol} is {current_price} and entry price is '
                                     f'{order.entry_price}, which is moving in the wrong direction for a '
                                     f'{order.direction} trade so we adjust entry to be {new_entry}')
                # If entry order is entered and executed:
                else:
                    # If price is target or better and no closing trade has been entered: enter limit trade to close out
                    if at_or_better_than(current_price, order.target_price, order.direction) \
                            and not order.closing_order_tag:
                        side = 'SELL' if order.direction == OrderDirection.LONG else 'BUY'
                        price_type = 'Limit'
                        logging.info(f'Target price of {order.target_price} reached for {order.symbol} (current price: '
                                     f'{current_price}). Sending {side} {price_type} order to close out.')
                        order.closing_order_tag = str(uuid.uuid4())
                        success, order_response = submit_order(
                            ord_stub=ord_stub, util_stub=util_stub, symbol=order.symbol, side=side,
                            quantity=order.quantity, route=order.route, account=order.account,
                            order_tag=order.closing_order_tag, price_type=price_type, user_token=user_token,
                            closing_order=True, limit_price=order.target_price)
                        if success:
                            logging.info(f'Closing order at target successfully submitted with order details: '
                                         f'{order_response}')
                            if order_response:
                                order.closing_order_id = order_response['OrderId']
                        else:
                            order.closing_order_tag = None
                            logging.warning(f'Closing order at target failed to submit. Order response: '
                                            f'{order_response}')
                    # If price is $0.10 or better: Change stop-loss price to 50%
                    elif at_or_better_than(current_price, order.near_target, order.direction) \
                            and not at_or_better_than(order.stop_loss_price, order.half_target, order.direction):
                        logging.info(f'{order.symbol} has reached near_target price of {order.near_target} (current '
                                     f'price: {current_price}). Setting stop_loss_price to half_target price of: '
                                     f'{order.half_target}')
                        order.stop_loss_price = order.half_target
                    # If price is 50% or better: Change stop-loss price to entry price
                    elif at_or_better_than(current_price, order.half_target, order.direction) \
                            and not at_or_better_than(order.stop_loss_price, order.entry_price, order.direction):
                        logging.info(f'{order.symbol} has reached half_target price of {order.half_target} (current '
                                     f'price: {current_price}). Setting stop_loss_price to entry price of: '
                                     f'{order.entry_price}')
                        order.stop_loss_price = order.entry_price
                    # If price is stop-loss or worse: Enter market or limit order to close out
                    elif at_or_worse_than(current_price, order.stop_loss_price, order.direction) \
                            and not stop_loss_order_submitted:
                        logging.info(f'Stop-loss price of {order.stop_loss_price} reached for {order.symbol} (current '
                                     f'price: {current_price})')
                        # First check if there is an open closing order already. This can occur if target price was
                        # reached and a limit order was sent to close out at target, and then the price kept falling and
                        # the trade was never executed
                        if order.closing_order_tag:
                            logging.info(f'Cancelling unexecuted closing order (OrderId={order.closing_order_id}) for '
                                         f'{order.symbol}')
                            cancel_response = cancel_order(ord_stub=ord_stub, user_token=user_token,
                                                           order_id=order.closing_order_id)
                            if cancel_response.ServerResponse.upper() == 'SUCCESS':
                                logging.info(f'Successfully cancelled order: {order.closing_order_id}')
                                order.closing_order_tag = None
                            else:
                                logging.warning(f'Failed to cancel order: {order.closing_order_id}. Please address!')
                        side = 'SELL' if order.direction == OrderDirection.LONG else 'BUY'
                        # TODO Make default to Market, and limit only if entered
                        price_type = 'Limit' if order.stop_loss_order_type == OrderType.LIMIT else 'Market'
                        limit_price = order.stop_loss_price if order.stop_loss_order_type == OrderType.LIMIT else None
                        logging.info(f'Sending {side} {price_type} order to close out (at stop loss)')
                        order.closing_order_tag = str(uuid.uuid4())
                        success, order_response = submit_order(
                            ord_stub=ord_stub, util_stub=util_stub, symbol=order.symbol, side=side,
                            quantity=order.quantity, route=order.route, account=order.account,
                            order_tag=order.closing_order_tag, price_type=price_type, user_token=user_token,
                            closing_order=True, limit_price=limit_price)
                        if success:
                            logging.info(f'Closing order at stop-loss successfully submitted with order details: '
                                         f'{order_response}')
                            stop_loss_order_submitted = True
                            if order_response:
                                order.closing_order_id = order_response['OrderId']
                        else:
                            order.closing_order_tag = None
                            logging.warning(f'Closing order at stop-loss failed to submit. Order response: '
                                            f'{order_response}')

    except Exception as e:
        logging.exception(f'Exception occurred in thread [{threading.current_thread().name}] of type: '
                          f'{type(e).__name__} with args: {e.args}')


def setup_test_orders(md_stub, user_token, order_info):
    test_orders = []
    for info in order_info:
        symbol = info[0]
        margin = info[1]
        direction = info[2]
        has_entry_limit = info[3]
        success, current_price = get_current_stock_price(md_stub, user_token, symbol)
        entry_price = round(current_price + 0.02 if direction == OrderDirection.LONG else current_price - 0.02, 2)
        stop_loss_price = round(entry_price - margin if direction == OrderDirection.LONG else current_price + margin, 2)
        target_price = round(entry_price + margin if direction == OrderDirection.LONG else current_price - margin, 2)
        half_target = round((entry_price + target_price) / 2, 2)
        near_target = round((half_target + target_price) / 2, 2)
        entry_limit = round((entry_price + half_target) / 2, 2) if has_entry_limit else None
        test_orders.append(
            BracketOrder(route='DEMO', account='EMSTEST;EMSTEST;APIDEMO;DEMO07', symbol=symbol, quantity=3,
                         direction=direction, entry_price=entry_price, stop_loss_price=stop_loss_price,
                         target_price=target_price, entry_limit=entry_limit,
                         half_target=half_target, near_target=near_target)
        )
    return test_orders


if __name__ == '__main__':
    # Read in file
    # load each trade into an array of BracketOrders
    # orders = []
    # Use time in force of day or day plus?
    # Only can use Stop limit order
    # orders.append(
    #     BracketOrder(route='DEMO', account='EMSTEST;EMSTEST;EMSUAT;XAPITEST001', symbol='DOW', quantity=3,
    #                  direction=OrderDirection.LONG, entry_price=53.42, stop_loss_price=53.39, target_price=53.48,
    #                  entry_order_type=OrderType.MARKET, entry_limit=None, half_target=53.45, near_target=53.47)
    # )

    with open(r'.\roots.pem', 'rb') as f:
        cert = f.read()
    server = 'chixapi.taltrade.com'
    port = '9000'
    main_channel = grpc.secure_channel(f'{server}:{port}', grpc.ssl_channel_credentials(root_certificates=cert))
    logging.info(f'Channel: {main_channel}')
    util_stub_main = util_grpc.UtilityServicesStub(main_channel)

    connect_response = None
    try:
        connect_response = login(util_stub=util_stub_main)

        md_stub_main = md_grpc.MarketDataServiceStub(main_channel)
        # ord_stub_main = ord_grpc.SubmitOrderServiceStub(channel)

        # aapl_tag = str(uuid.uuid4())
        # response_AAPL = ord_stub_main.SubmitSingleOrder(
        #     ord.SubmitSingleOrderRequest(Symbol='AAPL', Side='BUY', Quantity=3, Route='DEMO', OrderTag=aapl_tag,
        #                                  Account='EMSTEST;EMSTEST;EMSUAT;XAPITEST001',
        #                                  UserToken=connect_response.UserToken, ReturnResult=False)
        # )
        # logging.info(f'response_AAPL {aapl_tag}: {response_AAPL}')
        #
        # amzn_tag = str(uuid.uuid4())
        # response_AMZN = ord_stub_main.SubmitSingleOrder(
        #     ord.SubmitSingleOrderRequest(Symbol='AMZN', Side='BUY', Quantity=3, Route='DEMO', OrderTag=amzn_tag,
        #                                  Account='EMSTEST;EMSTEST;EMSUAT;XAPITEST001',
        #                                  UserToken=connect_response.UserToken, ReturnResult=False)
        # )
        # logging.info(f'response_AMZN {amzn_tag}: {response_AMZN}')

        # activity_response = util_stub_main.GetTodaysActivityJson(
        #     util.TodaysActivityJsonRequest(IncludeUserSubmitOrder=True, UserToken=connect_response.UserToken))
        #
        # df = pd.read_json(activity_response.TodaysActivityJson, orient='records')
        # order_details = df.loc[df['OrderTag'] == '881acbd1-b209-444d-8d00-67c013bdf03a']
        # orders_details = order_details.to_dict('records')
        #
        # logging.info(f'df index: {df.index}')
        # logging.info(f'df columns: {df.columns}')
        # print_info(order_details, 'order_details')
        # logging.info(f'orders_details len: {len(orders_details)}')
        # logging.info(f'orders_details: {orders_details}')
        # print_info(orders_details[0]['AveragePrice'], 'ave price')
        #
        # raise Exception('Ending early...')

        orders = setup_test_orders(md_stub_main, connect_response.UserToken, [
            # ['BRO', .20],
            ['PFGC', .15, OrderDirection.LONG, True],
            ['CIEN', .20, OrderDirection.LONG, False],
            ['BF.B', .20, OrderDirection.SHORT, True],
            ['OKE', .15, OrderDirection.SHORT, False],
        ])

        # order = BracketOrder(
        #     route='DEMO', account='EMSTEST;EMSTEST;EMSUAT;XAPITEST001', symbol='AGR', quantity=3,
        #     direction=OrderDirection.LONG, entry_price=35.10, stop_loss_price=34.70, target_price=35.69,
        #     entry_order_type=OrderType.MARKET, entry_limit=None, half_target=35.37, near_target=35.59)
        # ord_stub = ord_grpc.SubmitOrderServiceStub(channel)
        # side = 'BUY' if order.direction == OrderDirection.LONG else 'SELLSHORT'
        # price_type = 'StopLimit' if order.entry_limit else 'StopMarket'
        # logging.info(f'Submitting {side} {price_type} entry order for {order.symbol}')
        # order.order_tag = str(uuid.uuid4())
        # order_response = submit_order(
        #     ord_stub=ord_stub, symbol=order.symbol, side=side, quantity=order.quantity,
        #     route=order.route, account=order.account, order_tag=order.order_tag, price_type=price_type,
        #     user_token=connect_response.UserToken, closing_order=False, limit_price=order.entry_limit,
        #     stop_price=order.entry_price)
        # logging.info(f'Order result: {order_response}')
        # if order_response.ServerResponse != 'success':
        #     logging.warning('Entry order failed to submit')

        threads = [Thread(target=handle_order, args=(main_channel, connect_response.UserToken, order)) for order in orders]
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
        logging.info(f'Finished run for {trading_day}')
    except Exception as e:
        logging.exception(f'Exception occurred of type: {type(e).__name__} with args: {e.args}')
    finally:
        if connect_response and connect_response.Response == 'success':
            logging.info(f'Attempting to log out of account...')
            disconnect_response = util_stub_main.Disconnect(util.DisconnectRequest(UserToken=connect_response.UserToken))
            logging.info(f'Disconnect result: {disconnect_response.ServerResponse}')
