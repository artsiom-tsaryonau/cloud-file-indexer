import pickle
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SERVICE_ACCOUNT_FILE = 'gcredentials.json'

def __create_client(type):
    if type == 'gdrive 1':
        return GDriveClientWrapper(SERVICE_ACCOUNT_FILE)
    elif type == 'mega':
        pass
        
class GDriveClientWrapper:
    def __init__(self, credentials_file):
        self.creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.client = build('drive', 'v3', credentials=self.creds)

    def __find_folder_id(self, folder):
        results = self.client \
            .files() \
            .list(
                q="mimeType='application/vnd.google-apps.folder' and name='" + folder + "'",
                spaces='drive',
                fields='files(id, name)') \
            .execute() \
            .get('files', [])
        return results[0]["id"]   
    
    # implement recursive search
    def list_files(self, folder=None):
        folder_id = self.__find_folder_id(folder)
        files = []
        page_token = None
        while True:
            response = self.client \
                .files() \
                .list(
                    q="parents in '" + folder_id + "'", 
                    spaces='drive', 
                    fields='nextPageToken, files(id, name)',
                    pageToken=page_token) \
                .execute();
            files += [file['name'] for file in response.get('files', [])]
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return files
                
google_drive_client = __create_client('gdrive 1')
items = google_drive_client.list_files('books')
print('Number of books: {}'.format(len(items)))
