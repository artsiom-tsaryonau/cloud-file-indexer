import itertools
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

class CloudClientFactory:
    def get_client(self, type, *constructor_args):
        if type == 'gdrive 1':
            return GDriveClientWrapper(constructor_args[0])
        elif type == 'mega':
            pass

class GDriveClientWrapper:
    def __init__(self, credentials_file):
        self.creds = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES)
        self.client = build('drive', 'v3', credentials=self.creds)

    # returns list as there might be multiple folders with the same name
    def __find_folder_ids(self, folder):
        results = self.__do_search(
            "mimeType='application/vnd.google-apps.folder' and name='" + folder + "'", 
            'nextPageToken, files(id, name)') 
        return [result["id"] for result in results]
    
    # TODO: implement recursive search
    def __list_files(self, folder, types=None):
        folder_ids = self.__find_folder_ids(folder)
        all_files = []
        for folder_id in folder_ids:
            # ugly
            if types is None:
                query="parents in '" + folder_id + "'"
            else:
                types_str = ' or '.join(["mimeType='" + type + "'" for type in types])
                query=types_str + " and parents in '" + folder_id + "'"
            all_files += self.__do_search(query, 'nextPageToken, files(id, name, mimeType)')
        return all_files
        
    def __do_search(self, query, fields):
        results = []
        page_token = None
        while True:
            response = self.client \
                .files() \
                .list(q=query, spaces='drive', fields=fields, pageToken=page_token) \
                .execute()
            results += response.get('files', [])
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return results

    def list_files(self, folder, types):
        return [file['name'] for file in self.__list_files(folder, types)]
        
    # for now I combine all folders - shared and regular into the same set
    def folder_stats(self, folder):
        files = self.__list_files(folder)
        stats = {}
        for key, group in itertools.groupby(sorted(files, key=lambda item: item['mimeType']), lambda file: file["mimeType"]):
            stats[key] = len(list(group))
        return stats