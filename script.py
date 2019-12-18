
from mega import Mega

mega = Mega().login('sebastrident@gmail.com', 'Star treksg-11992')
details = mega.get_user()
print(mega.find('build tools'))

# two main pipelines
'''
    1. cloud pipeline
        - connect to cloud storage
        - list files from the book folder
    
    2. normalization pipeline
        - get book archive file name
        - remove extension
        - split by first '-'
        - create a tuple in format: [publisher;title;subtitle;cloud]
    
    3. export as CSV
'''


'''
    # mega.nz
    cloud_pipeline = MegaPipeline(login, password)
    list = cloud_pipeline.list_files('books', recursively=True)
    
    # google drive
    cloud_pipeline = GoogleDrivePipeline(credentials.file)
    list = cloud_pipeline.list_files('books', recursively=True)
    
    normalized_list = NormalizerPipeline().normalize(list)
    assign_tag(list, 'gdrive | mega')
    
    export_to_csv(list)
    export_to_csv(list)
'''