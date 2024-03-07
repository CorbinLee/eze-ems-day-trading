import pandas as pd
import logging
import math

from bracket_order import OrderDirection
from bracket_order import OrderType
from bracket_order import BracketOrder


class OrderCsvReader:
    """Reads Order CSV rows and parses them into BracketOrder objects"""

    def __init__(self, filepath):
        """
        :param filepath: Full or relative file path of the CSV file holding the bracket orders
        """
        self.filepath = filepath

    def read_orders(self, account):
        orders_df = pd.read_csv(self.filepath)
        # Replace NaN values with None
        pd.set_option('display.max_columns', None)  # todo remove
        orders_df.replace(math.nan, None, inplace=True)
        # Convert strings to enums
        logging.info(orders_df)
        orders_df['Direction'] = orders_df['Direction'].apply(lambda x: OrderDirection[x])
        orders_df['Stop Loss Order Type'] = orders_df['Stop Loss Order Type'].apply(
            lambda x: OrderType.LIMIT if x is None else OrderType[x])
        logging.info(orders_df)
        csv_orders = []
        for i, row in orders_df.iterrows():
            if row['Half Target Price'] is None:
                if row['Direction'] == OrderDirection.LONG:
                    row['Half Target Price'] = math.floor(100 * (row['Entry Price'] + row['Target Price']) / 2) / 100
                else:
                    row['Half Target Price'] = math.ceil(100 * (row['Entry Price'] + row['Target Price']) / 2) / 100
            if row['Near Target Price'] is None:
                row['Near Target Price'] = row['Target Price'] - (
                    0.10 if row['Direction'] == OrderDirection.LONG else -0.10)

            csv_orders.append(
                BracketOrder(account=account, route=row['Route'], symbol=row['Symbol'], quantity=row['Quantity'],
                             direction=row['Direction'], entry_price=row['Entry Price'], entry_limit=row['Entry Limit'],
                             stop_loss_price=row['Stop Loss Price'], stop_loss_order_type=row['Stop Loss Order Type'],
                             target_price=row['Target Price'], half_target=row['Half Target Price'],
                             near_target=row['Near Target Price']))
            logging.info(csv_orders[-1])
        return csv_orders
