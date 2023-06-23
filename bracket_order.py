from enum import Enum
import uuid


class OrderType(Enum):
    LIMIT = 1
    MARKET = 2


class OrderDirection(Enum):
    LONG = 1
    SHORT = 2


class BracketOrder:
    """Class representing a bracket order"""

    def __init__(self, route, account, symbol, quantity, direction, entry_price, stop_loss_price, target_price,
                 entry_order_type=OrderType.LIMIT, stop_loss_order_type=OrderType.LIMIT, entry_limit=None,
                 half_target=None, near_target=None):
        """
        :param route: Route name as shown in Eze EMS (i.e.  ARCA-LS, NYSE-LS, etc.)
        :param account: Semi colon separated values that represent the account this trade is for (i.e. TAL;TEST;USER1;TRADE)
        :param symbol: Stock symbol that this order is working on
        :param quantity: Number of shares to either buy or sell short
        :param direction: SHORT or LONG depending on whether we want to buy or sell short the stock shares
        :param entry_price: Entry price to enter into the order at
        :param stop_loss_price: Stop loss price which will be the price at the bottom of the bracket order
        :param target_price: Target price which will be the price at the top of the bracket order
        :param entry_limit: Limit price for the initial order
        :param entry_order_type: Type of order to make for the entry order (LIMIT or MARKET)
        :param stop_loss_order_type: Type of order to make for the stop-loss order (LIMIT or MARKET)
        :param half_target: Optional parameter representing the first point where the stop-loss should be moved if
            reached, usually halfway between the entry and target prices
        :param near_target: Optional parameter representing the second point where the stop-loss should be moved if
            reached, usually $0.10 to the target price
        """
        self.route = route
        self.account = account
        self.symbol = symbol
        self.quantity = quantity
        self.direction = direction
        self.entry_price = entry_price
        self.stop_loss_price = stop_loss_price
        self.target_price = target_price
        self.entry_limit = entry_limit
        self.entry_order_type = entry_order_type
        self.stop_loss_order_type = stop_loss_order_type
        self.half_target = half_target
        self.near_target = near_target
        # Unique tag used to identify this order
        self.order_tag = None
        # ID assigned by server after order has been entered
        self.order_id = None
        # Order tag for the closing order once it's been created
        self.closing_order_tag = None
        # Order ID for the closing order once it's been created
        self.closing_order_id = None

    def __str__(self):
        return f'BracketOrder(route={self.route},account={self.account},symbol={self.symbol},' \
               f'quantity={self.quantity},direction={self.direction},entry_price={self.entry_price},' \
               f'stop_loss_price={self.stop_loss_price},target_price={self.target_price},' \
               f'entry_limit={self.entry_limit},entry_order_type={self.entry_order_type},' \
               f'stop_loss_order_type={self.stop_loss_order_type},half_target={self.half_target},' \
               f'near_target={self.near_target},order_tag={self.order_tag},order_id={self.order_id},' \
               f'closing_order_tag={self.closing_order_tag},closing_order_id={self.closing_order_id})'
