# step one: download and install packages using pip (Python's package installer)
# -> target Python 3 using 'pip3'
# -> instruct pip to install the packages using the subcommand 'install'
# -> insert the name of the first package 'gspread' (a Python API for Google Sheets)
# -> insert the name of the second package 'google-auth' (a Python library for authenticating with Google service, incl. G-Sheets)
# Note: these packages must be installed, as they are not part of the standard Python library.

# imports the gspread API
import gspread
# imports the google-auth library and 'Credentials' class from google.oauth2.service_account module
# Note: The 'Credentials' class represents the credentials used to authenticate requests to Google APIs
from google.oauth2.service_account import Credentials

# These strings represent the different scopes or permissions 
# required by the Google Sheets API and Google Drive API to perform certain actions. 
SCOPE = [
    # grants read and write access to Google Sheets documents
    "https://www.googleapis.com/auth/spreadsheets",
    # grants access to files created or opened by the app
    "https://www.googleapis.com/auth/drive.file",
    # grants full access to Google Drive, including files, folders, and metadata
    "https://www.googleapis.com/auth/drive"
    ]
# loads credentials from a service account file named 'creds.json'
# note: service account credentials are used to authenticate your application when accessing G-APIs programmatically
CREDS = Credentials.from_service_account_file('creds.json')
# credentials loaded in the previous step (CREDS) are augmented with the specified scopes (SCOPE)
# note: scopes define the permissions that your application requires to access specific G-APIs
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# authorizes the G-Sheets API client (gspread) using the scoped credentials (SCOPED_CREDS)
# note: the authorize() function creates an authorized client object that can be used to interact with G-Sheets
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# opens a G-Sheets document named 'love_sandwiches' using the authorized client (GSPREAD_CLIENT)
# note: the open() function returns a Spreadsheet object representing the specified G-Sheets document, 
# which can then be used to read or modify its contents.
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# Tl;Dr: In summary, these 4 lines of code initialise the necessary components for the application to interact with G-Sheets: 
# loading credentials, specifying scopes, authorizing the client, and opening the desired G-Sheets document.

# retrieves a specific worksheet named 'sales' from the G-Sheets document opened earlier (SHEET)
sales = SHEET.worksheet('sales')

# retrieve the data contained in the love_sandwiches G-Sheet
data = sales.get_all_values()
# view the data in the console
print(data)