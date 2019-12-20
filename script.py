import os, csv, itertools
from cloud import CloudClientFactory

SERVICE_ACCOUNT_FILE = 'gcredentials.json'
                            
class FileNameNormalizerChain:
    def normalize(self, filename, tag):
        filename = self.__drop_extension(filename)
        filename = self.__utf_8(filename)
        split = self.__split_titles(filename)
        return self.__taggify(split, tag)
        
    def __taggify(self, filename_tuple, tag):
        return filename_tuple + (tag,)
        
    def __drop_extension(self, filename):
        return os.path.splitext(filename)[0]
        
    def __split_titles(self, filename):
        index = filename.index('-')
        return (filename[:index].rstrip(), filename[index+1:].lstrip())
        
    def __utf_8(self, filename):
        return filename.encode("utf-8")

# download from google drive
google_drive_client = CloudClientFactory().get_client('gdrive 1', 'gcredentials.json')
items = google_drive_client.list_files('books', ['application/x-rar', 'application/rar'])

# normalize
normalizer = FileNameNormalizerChain()
items = [normalizer.normalize(filename, 'gdrive') for filename in items]

print(google_drive_client.folder_stats('books'))
print(len(items))

with open('books.csv', mode='w') as csv_books:
    csv_writer = csv.writer(csv_books, delimiter=',', quoting=csv.QUOTE_ALL)
    for file_row in sorted(items, key=lambda tuple: tuple[0]):
        csv_writer.writerow(file_row)

