import csv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from configparser import ConfigParser

# Get config
config = ConfigParser()
config.read('config/config.ini')

# Set the Google Workspace domain and API Version
domain = config['workspace']['domain']
admin_email = config['workspace']['admin email']
version = config['workspace']['api version']

# Set group name and email
group_name = config['workspace']['group name']
group_email = group_name + "@" + domain

# Set the credentials for your Google Workspace service account
service_account_credentials = config['credentials']['service account']
creds = service_account.Credentials.from_service_account_file(
    service_account_credentials,
    scopes=['https://www.googleapis.com/auth/admin.directory.group.member'],
    subject=admin_email
)

# Create a service object for the Google Workspace API
service = build('admin', version, credentials=creds)

# Set the path to the CSV file containing user data
csv_path = config['files']['users csv']

# Open the CSV file and read the user data
with open(csv_path, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for row in reader:
        # Extract the user data from the CSV row
        firstname, lastname, password, title = row

        user_email = firstname + "@" + domain

        member = {'email': user_email,}

        try:
            # Create the user using the Google Workspace API
            result = service.members().insert(groupKey=group_email, body=member).execute()
            
            # Print the result
            print("User " + user_email + " was added to the " + group_name + " group successfully")

        except HttpError as err:
            if err.reason == "Member already exists.":
                print("User " + user_email + " is already a member of the " + group_name + " group")
            else:
                print("There was an error adding user " + user_email + " to the " + group_name + " group. Error: " + err.reason)
