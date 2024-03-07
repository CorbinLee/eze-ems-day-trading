# Guide For Use
## Overview


## How It Works


## Input CSV file
### Format
The orders to be executed for a given day should be written into a CSV file with the columns:
1. `Symbol` - The ticker symbol for the stock to be traded
2. `Route` - Route for this trade, i.e. ARCA-LS, NYSE-LS, etc.
3. `Quantity` - The number of stocks to be traded
4. `Direction` - Can be either LONG or SHORT
5. `Entry Price` - Price to set as the Stop Price for the entry order
6. `Entry Limit` *(Optional)* - Limit Price for the entry order. If blank, the entry order will be sent as a Market Order
7. `Stop Loss Price` - Stop Loss price that will trigger a closing order if hit to prevent further losses
8. `Stop Loss Order Type` *(Optional)* - Can be either MARKET or LIMIT. Will default to LIMIT
9. `Target Price` - Target price that will trigger a closing order if hit to lock in profits at
10. `Half Target Price` *(Optional)* - First threshold price when hit, will cause the Stop Loss Price to move to the Entry Price. If absent this will default to the midpoint between Entry Price and Target Price (rounding away from Target Price)
11. `Near Target Price` *(Optional)* - Second threshold price when hit, will cause the Stop Loss Price to move to the Half Target Price. If blank, this will default to Target Price - $0.10 for LONG orders, and + $0.10 for SHORT orders

### File Name and Location 
The CSV file should be named like `{trading day}_orders.csv`, i.e. `2024-03-01_orders.csv`. To have the program use a custom file name, run it with a command line argument specifying the full file name, i.e. 
```commandline
python main.py custom_file_name.csv
```

The CSV file must be put in the folder named: `input_orders`

### File Template
A template file with all the correct headers can be found [here](https://docs.google.com/spreadsheets/d/1CDK9tDefJBgzsxxPt-_WxIMnwZl2x2n70DY_S7jI4xo/edit?usp=sharing)

## Rules
* There must be only one trade per symbol.
* The order prices must be as such for LONG orders: Stop Loss < Entry < Half Target < Near Target < Target. And vice versa for SHORT orders.
* 