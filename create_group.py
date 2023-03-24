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
    scopes=['https://www.googleapis.com/auth/admin.directory.group'],
    subject=admin_email
)

# Create a service object for the Google Workspace API
service = build('admin', version, credentials=creds)

# Define the properties of the group
group = {
    'email': group_email,
    'name': group_name,
    'whoCanJoin': 'INVITED_CAN_JOIN',
    'whoCanViewMembership': 'ALL_IN_DOMAIN_CAN_VIEW',
    'whoCanPostMessage': 'ALL_IN_DOMAIN_CAN_POST',
    'allowExternalMembers': False,
    'membersCanPostAsTheGroup': False,
    'sendEmailToMembers': True,
    'allowWebPosting': True,
    'maxMessageBytes': 2048,
    'isArchived': False
}

try:
    # Call the API to create the group
    response = service.groups().insert(body=group).execute()

    print('Group created: %s' % response['email'])
except HttpError as err:
    if err.reason == "Entity already exists.":
        print("Group " + group_name + " already exists.")
    else:
        print("There was an error creating group " + group_name + ". Error: " + err.reason)