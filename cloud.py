import itertools
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

class CloudClientFactory:
    def get_client(self, type, *constructor_args):
        if type == 'gdrive':
            return GDriveClientWrapper(constructor_args[0])
        elif type == 'mega':
            pass

class GDriveQuery:
    def __init__(self, mime_types, name=None, parents=None):
        self.mime_types = mime_types
        self.name = name
        self.parents = parents
        
    def build(self):
        full_filter = []
        full_filter += ' or '.join(["mimeType='" + type + "'" for type in mime_types])
        if parents:
            full_filter += ' and '.join(["'" + parent_id + "' in parents" for parent_id in parents]) 
        if name:
            full_filter += "name='" + name + "'"
        query = ' and '.join(full_filter)
        print(query)
        return query
      
class GDriveIndexer:
    def __init__(self, client):
        self.client = client
        
    def do_search(self, query, fields):
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

class GDriveClientWrapper:
    def __init__(self, credentials_file):
        self.indexer = GDriveIndexer(build('drive', 'v3', 
            credentials=service_account.Credentials.from_service_account_file(credentials_file, scopes=SCOPES))

    # returns list as there might be multiple folders with the same name
    def __find_folder_ids(self, folder):
        query_builder = GDriveQuery(['application/vnd.google-apps.folder'], folder)
        results = self.indexer.do_search(query_builder.build(), 'nextPageToken, files(id, name)') 
        return [result["id"] for result in results]
    
    # TODO: implement recursive search
    def __list_files(self, folder, types=None):
        folder_ids = self.__find_folder_ids(folder)
        all_files = []
        for folder_id in folder_ids:
            query_builder = GDriveQuery(types, parents=[folder_id])
            all_files += self.indexer.do_search(query_builder.build(), 'nextPageToken, files(id, name, mimeType)')
        return all_files
        
    def list_files(self, folder, types):
        return [file['name'] for file in self.__list_files(folder, types)]
        
    # for now I combine all folders - shared and regular into the same set
    def folder_stats(self, folder):
        files = self.__list_files(folder)
        stats = {}
        for key, group in itertools.groupby(sorted(files, key=lambda item: item['mimeType']), lambda file: file["mimeType"]):
            stats[key] = len(list(group))
        return stats