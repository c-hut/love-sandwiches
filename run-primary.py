import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
 
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

sales_worksheet = SHEET.worksheet('sales')
surplus_worksheet = SHEET.worksheet('surplus')

def get_sales_data():
    """
    Retrieve sales figures input from the user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10, 20, 30, 40, 50, 60\n")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(", ")

        if validate_data(sales_data):
            print('Input successfully processed. Thank you.\n')
            sales_data = [int(value) for value in sales_data]
            break
    return sales_data

def validate_data(values):
    """
    Validate data provided by the user
    """
    try:
        invalid_chars = []
        converted_values = []

        for val in values:
            if not str(val).isdigit():
                invalid_chars.append(val)
            else:
                converted_values.append(int(val))
        if invalid_chars:
            raise ValueError(f"expected only numbers but received {invalid_chars} as input")
        elif len(values) != 6:
            raise ValueError(
                f"expected 6 values but received {len(values)} instead"
            )
    except ValueError as e:
        print(f"Invalid data: {e}. Please try again.\n")
        return False
    
    return True

def calculate_surplus_data(last_row_sales):
    """ 
    Calculate the surplus for each sandwich type

    Calculation: stock - sales = surplus
    - positive surplus indicates wasted sandwiches
    - negative surplus indicates additional sandwiches
    """

    print("Calculating surplus data...\n")
    stock_worksheet = SHEET.worksheet('stock')
    stock_data = stock_worksheet.get_all_values()
    total_rows = len(stock_worksheet.col_values(1))
    last_row_stock = stock_worksheet.row_values(total_rows)

    surplus_data = []
    for stock, sales in zip(last_row_stock, last_row_sales):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def update_worksheet(data, worksheet, worksheet_name):
    """
    Update worksheets: add new sales and surplus data
    """
    print(f"Updating {worksheet_name} worksheet...\n")
    worksheet.append_row(data)
    print(f"{worksheet_name.capitalize()} worksheet updated successfully.\n")

def get_last_5_sales_entries():
    """
    Collects the last 5 sales entries for each sandwich (data format: list of lists)
    """
    columns = []
    # for each value in range: 1 - 6 (inclusive)...
    for num in range(1,7):
        #...use the column total, which is 6...
        column = sales_worksheet.col_values(num)
        #...append each column (stored as a list) and its values to the columns list
        #--> note: slice after retrieving all column data first,
        # as opposed to only retrieving the last 5 entries - a more flexible approach
        columns.append(column[-5:])
    return columns

def program():
    sales_data = get_sales_data()
    update_worksheet(sales_data, sales_worksheet, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, surplus_worksheet, "surplus")

print("Welcome to Love Sandwiches Data Automation\n")
# program()

sales_columns = get_last_5_sales_entries()