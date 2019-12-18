import pickle
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SERVICE_ACCOUNT_FILE = 'gcredentials.json'

def __create_client(type):
    if type == 'gdrive':
        return GDriveClientWrapper(SERVICE_ACCOUNT_FILE)
    elif type == 'mega':
        pass
        
class GDriveClientWrapper:
    def __init__(self, credentials_file):
        self.creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.client = build('drive', 'v3', credentials=self.creds)
        
    def list_files(self, folder, recursive=False):
        return self.client.files().list(q = "mimeType='application/vnd.google-apps.folder' and name='books'", 
                  spaces='drive',
                  fields='nextPageToken, files(id, name)').execute().get('files', [])
                
google_drive_client = __create_client('gdrive')
items = google_drive_client.list_files('')
if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))