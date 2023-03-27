import csv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from configparser import ConfigParser

import sys
sys.path.append("helpers")
from random_password_generator import genrateRandomPassword

# Get config
config = ConfigParser()
config.read('config/config.ini')

# Set the Google Workspace domain and API Version
domain = config['workspace']['domain']
admin_email = config['workspace']['admin email']
version = config['workspace']['api version']

# Set the credentials for your Google Workspace service account
service_account_credentials = config['credentials']['service account']
creds = service_account.Credentials.from_service_account_file(
    service_account_credentials,
    scopes=['https://www.googleapis.com/auth/admin.directory.user'],
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
        firstname, lastname, title = row

        # Set the user object for the Google Workspace API
        user = {
            'name': {
                'givenName': firstname,
                'familyName': lastname
            },
            'primaryEmail': firstname + "@" + domain,
            'password': genrateRandomPassword(),
            'changePasswordAtNextLogin': True, # prompts a mandatory password change upon first use
            'organizations': [
                {
                    'title': title
                }
            ]
        }

        try:
            # Create the user using the Google Workspace API
            result = service.users().insert(body=user).execute()

            # Print the result and Email (one-time) password
            print("User " + result["primaryEmail"] + " created. Default password: " + user["password"])

        except HttpError as err:
            if err.reason == "Entity already exists.":
                print("User " + user["primaryEmail"] + " already exists.")
            else:
                print("There was an error creating user " + user["primaryEmail"] + ". Error: " + err.reason)
