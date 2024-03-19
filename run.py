# step one: download and install packages using pip (Python's package installer)
# -> target Python 3 using 'pip3'
# -> instruct pip to install the packages using the subcommand 'install'
# -> insert the name of the first package 'gspread' (a Python API for Google Sheets)
# -> insert the name of the second package 'google-auth' (a Python library for authenticating with Google service, incl. G-Sheets)
# Note: these packages must be installed, as they are not part of the standard Python library.

# step 2: import the gspread API
import gspread

# step 3: import libraries and classes

# import the google-auth library and 'Credentials' class from google.oauth2.service_account module
# Note: The 'Credentials' class represents the credentials used to authenticate requests to Google APIs
from google.oauth2.service_account import Credentials

# import pprint()
from pprint import pprint

# step 4: define scopes and permissions

# explanation: these strings represent the scopes and permissions required by the G-Sheets and G-Drive APIs to perform certain actions 
SCOPE = [
    # grants read and write access to Google Sheets documents
    "https://www.googleapis.com/auth/spreadsheets",
    # grants access to files created or opened by the app
    "https://www.googleapis.com/auth/drive.file",
    # grants full access to Google Drive, including files, folders, and metadata
    "https://www.googleapis.com/auth/drive"
    ]
# step 5: load credentials, specify scopes, authorise the client, and open the desired G-Sheets document

# loads credentials from a service account file named 'creds.json'
# note: service account credentials are used to authenticate your application when accessing G-APIs programmatically
CREDS = Credentials.from_service_account_file('creds.json')
# credentials loaded in the previous step (CREDS) are augmented with the specified scopes (SCOPE)
# note: scopes define the permissions that your application requires to access specific G-APIs
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# authorizes the G-Sheets API client (gspread) using the scoped credentials (SCOPED_CREDS)
# note: the authorize() function creates an authorized client object that can be used to interact with G-Sheets
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# opens a G-Sheets document named 'love_sandwiches' using the authorised client (GSPREAD_CLIENT)
# note: the open() function returns a Spreadsheet object representing the specified G-Sheets document, 
# which can then be used to read or modify its contents.
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# step 7: retrieve the 'sales' worksheet from the G-Sheets document opened earlier (SHEET)
sales_worksheet = SHEET.worksheet('sales')
stock_worksheet = SHEET.worksheet('stock')

# step 8: check if the above code is functioning correctly (and comment it out once confirmed)

# retrieve the data contained in the love_sandwiches G-Sheet
# -> data = sales.get_all_values()
# view the data in the console
# - > print(data)

# write the program as reflected here: https://shorturl.at/dkwLW

# begin by retrieving the sales data from the user

def get_sales_data():
    # write a docstring explaining the purpose of the function
    """
    Retrieve sales figures input from the user
    """
    # add a while loop to ensure the program starts again upon incorrect entry of data
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10, 20, 30, 40, 50, 60\n")

        data_str = input("Enter your data here: ")
        # print(f"The data provided is as follows: {data_str}")

        sales_data = data_str.split(", ")

        if validate_data(sales_data):
            print('Input successfully processed. Thank you.\n')
            # convert the list of strings to integers
            sales_data = [int(value) for value in sales_data]
            break
    # return the validated data once valid user input has been identified
    return sales_data

# validate the data provided by the user
def validate_data(values):
    """
    Validate data provided by the user
    """
    # using 'try', attempt to execute statements that might raise an error
    try:
        # create an empty list to store the incorrect characters
        invalid_chars = []
        # create an empty list to store the converted values
        converted_values = []

        # iterate over the values and check if each value is a digit
        for val in values:
            if not str(val).isdigit():
                # if a value is not a digit, add it to the list of invalid characters
                invalid_chars.append(val)
            else:
                converted_values.append(int(val))
        # if there are any invalid characters, raise a 'ValueError' with a custom message
        if invalid_chars:
            #... raise a 'ValueError' w/ a custom message
            raise ValueError(f"expected only numbers but received {invalid_chars} as input")
        # if the length of the values list is not equal to 6...
        elif len(values) != 6:
            #... raise a 'ValueError' w/ a custom message
            raise ValueError(
                # input the length of the list containing the values
                f"expected 6 values but received {len(values)} instead"
            )
    except ValueError as e:
        print(f"Invalid data: {e}. Please try again.\n")
        return False
    
    return True

def update_sales_worksheet(sales_data, sales_worksheet):
    """
    Update sales worksheet: add a new row with and input validated data
    """
    # in the event of an error, adding print statements such as this one can provide clarity
    # as to the point at which the error occurred, i.e. if it occurred after this print statement,
    # it could be confirmed that the program reached this point before throwing an error
    print("Updating sales worksheet...\n")
    # grab the 'SHEET' variable defined at the top of the file
    # and use the worksheet() method to access the Sales sheet
    sales_worksheet.append_row(sales_data)
    print("Sales worksheet updated successfully.\n")

def calculate_surplus_data(last_row_sales):
    """ 
    Calculate the surplus for each sandwich type

    Calculation: stock - sales = surplus
    - positive surplus indicates wasted sandwiches
    - negative surplus indicates additional sandwiches
    """

    print("Calculating surplus data...\n")
    # save the retrieved stock data to a variable so that it can be used later
    stock_data = stock_worksheet.get_all_values()
    # use pprint to display the stock data in list format
    # --> pprint(stock_data)

    # retrieve data from the last row of the stock worksheet
    # --> calculate the total number of rows using the len() and col_values() methods
    total_rows = len(stock_worksheet.col_values(1))
     # the total_rows variable holds the number of rows, which equates to the last row number
     # --> note: negative indexing (stock_data[-1]) would result in errors in the case of empty rows
    last_row_stock = stock_worksheet.row_values(total_rows)
    # f-strings used to determine whether the correct data is returned
    #--> print(f'Here\'s the data from the last row in the stock worksheet: {last_row_stock}')
    #--> print(f'Here\'s the data from the last row in the stock worksheet: {last_row_sales}')

    # create an empty list within which the results of the below calculation will be stored
    surplus_data = []

    for stock, sales in zip(last_row_stock, last_row_sales):
        # use int() method to directly return the converted integer, as opposed to list comprehension
        surplus = int(stock) - sales
        # append the result to the surplus_data list above
        surplus_data.append(surplus)
    # return the result of the calculation
    return surplus_data

def program():
    # store the validated sales data in the reasssigned sales_data variable for later use
    sales_data = get_sales_data()
    # input the data into the sales G-Sheet
    update_sales_worksheet(sales_data, sales_worksheet)
    # calculate the surplus and input the data into the sales G-Sheet; assign the call to a variable
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)

print("Welcome to Love Sandwiches Data Automation\n")
program()