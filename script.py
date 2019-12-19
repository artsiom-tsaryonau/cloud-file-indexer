import os
import itertools
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
    
    # TODO: implement recursive search
    def __list_files(self, folder, types=None):
        folder_id = self.__find_folder_id(folder)
        
        # ugly
        if types is None:
            query="parents in '" + folder_id + "'"
        else:
            types_str = ' or '.join(["mimeType='" + type + "'" for type in types])
            query=types_str + " and parents in '" + folder_id + "'"
        
        files = []
        page_token = None
        while True:
            response = self.client \
                .files() \
                .list(q=query, spaces='drive', 
                    fields='nextPageToken, files(id, name, mimeType)',
                    pageToken=page_token) \
                .execute();
            files += response.get('files', [])
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return files
        
    def list_filenames(self, folder, types):
        return [file['name'] for file in self.__list_files(folder, types)]
        
    def folder_stats(self, folder):
        files = self.__list_files(folder)
        for key, group in itertools.groupby(sorted(files, key=lambda item: item['mimeType']), lambda file: file["mimeType"]):
            print("type: {} ; number of items: {}".format(key, len(list(group))))
              
              
class FileNameNormalizerChain:
    def normalize(self, filename, tag):
        filename = self.__drop_extension(filename)
        split = self.__split_titles(filename)
        return self.__taggify(split, tag)
        
    def __taggify(self, filename_tuple, tag):
        return filename_tuple + (tag,)
        
    def __drop_extension(self, filename):
        return os.path.splitext(filename)[0]
        
    def __split_titles(self, filename):
        index = filename.index('-')
        return (filename[:index].rstrip(), filename[index+1:].lstrip())

# download from google drive
google_drive_client = __create_client('gdrive 1')
items = google_drive_client.list_filenames('books', ['application/x-rar', 'application/rar'])

# normalize
normalizer = FileNameNormalizerChain()
items = [normalizer.normalize(filename, 'gdrive') for filename in items]
print(items)

