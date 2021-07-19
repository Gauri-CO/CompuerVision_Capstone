import os
from multiprocessing.pool import ThreadPool
from azure.storage.blob import BlobServiceClient, BlobClient
import yaml
from azure.storage.blob import ContentSettings, ContainerClient


def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))

    with open(dir_root + "/config.yaml", "r") as yamlfile:
        try:
            return yaml.load(yamlfile, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            print(e)


config =load_config()

MY_CONNECTION_STRING = config[0]["azure_storage_connectionstring"]

# Replace with blob container name
MY_BLOB_CONTAINER = config[0]["video_container_name"]

# Replace with the local folder where you want downloaded files to be stored
LOCAL_BLOB_PATH = config[0]["source_folder"] + "/downloads/"


class AzureBlobFileDownloader:
    def __init__(self):
        print("Intializing AzureBlobFileDownloader")

        # Initialize the connection to Azure storage account
        self.blob_service_client = BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
        self.my_container = self.blob_service_client.get_container_client(MY_BLOB_CONTAINER)


    def download_all_blobs_in_container(self):
        # get a list of blobs
        my_blobs = self.my_container.list_blobs()
        result = self.run(my_blobs)
        print(result)

    def run(self, blobs):
        # Download 10 files at a time!
        with ThreadPool(processes=int(10)) as pool:
            return pool.map(self.save_blob_locally, blobs)

    def save_blob_locally(self, blob):
        file_name = blob.name
        print(file_name)
        bytes = self.my_container.get_blob_client(blob).download_blob().readall()

        # Get full path to the file
        download_file_path = os.path.join(LOCAL_BLOB_PATH, file_name)
        # for nested blobs, create local path as well!
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)

        with open(download_file_path, "wb") as file:
            file.write(bytes)
        return file_name


# Initialize class and upload files
azure_blob_file_downloader = AzureBlobFileDownloader()
azure_blob_file_downloader.download_all_blobs_in_container()

print("Download completed successfully")