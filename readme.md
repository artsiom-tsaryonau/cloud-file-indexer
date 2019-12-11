# Description
The goal is to get the file list from cloud storage (mega & google drive) and parse into a corresponding structure.

# Build image

docker build -t cloud_file_indexer .

# Run image

docker run -it --rm -v c:/projects/cloud-file-index:/home/tmp cloud_file_indexer
