# step one: download and install packages using pip (Python's package installer)
# -> target Python 3 using 'pip3'
# -> instruct pip to install the packages using the subcommand 'install'
# -> insert the name of the first package 'gspread' (a Python API for Google Sheets)
# -> insert the name of the second package 'google-auth' (a Python library for authenticating with Google service, incl. G-Sheets)
# Note: these packages must be installed, as they are not part of the standard Python library.

# step 2: import the gspread API
import gspread
# step 3: import the google-auth library and 'Credentials' class from google.oauth2.service_account module
# Note: The 'Credentials' class represents the credentials used to authenticate requests to Google APIs
from google.oauth2.service_account import Credentials

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
sales = SHEET.worksheet('sales')

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
    print("Please enter sales data from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10, 20, 30, 40, 50, 60\n")

    data_str = input("Enter your data here: ")
    print(f"The data provided is as follows: {data_str}")

get_sales_data()