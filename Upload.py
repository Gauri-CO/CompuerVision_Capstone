import os
import yaml
import re
from azure.storage.blob import ContainerClient
import datetime


def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))

    with open(dir_root + "/config.yaml", "r") as yamlfile:
        try:
            return yaml.load(yamlfile, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            print(e)


def get_files(dir):
    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.is_file() and not entry.name.startswith("."):
                yield entry


def check_file(filename, filext):
    if filext == "csv":
        pattern = load_config()[0]["csv_file_pattern"]
    elif filext == "mp4":
        pattern = load_config()[0]["mp4_file_pattern"]
    elif filext == "avi":
        pattern = load_config()[0]["avi_file_pattern"]

    x = re.search(pattern, filename)
    if x:
        return True
    else:
        return False


def upload(files, connection_string, container_name, filext):
    container_client = ContainerClient.from_connection_string(connection_string, container_name)
    print("Uploading files to blob storage....")
    total_files = 0
    file_uploaded = 0

    for file in files:
        total_files = total_files + 1
        print(file.name)
        if check_file(file.name,filext):
            blob_client = container_client.get_blob_client(file.name)
            with open(file.path, "rb") as data:
                blob_client.upload_blob(data)
                # os.remove(file)
                print(f"{file.name} uploaded to blob storage")
                file_uploaded = file_uploaded + 1
        else:
            print(f"{file.name} is not uploaded to blob storage")

    print(f"Total number of files on local drive: {total_files}")
    print(f"Total number of files uploaded on Blob Storage: {file_uploaded}")


print(f"####File upload started at {datetime.datetime.now()}")
print(
    "------File Upload Service to Azure Blob Storage----- \n Filename pattern : VIRAT_S_XXYYZZ_KK_SSSSSS_TTTTTT_YYYYMMDD.mp4 \n XX: collection group ID \n YY: scene ID \n ""ZZ: sequence ID \n KK: segment ID (within sequence) \n SSSSSS: starting seconds in %06d format. E.g., ""1 min 2 sec is 000062. \n TTTTTT: ending seconds in %06d format \n YYYYMMDD: Date when video was recorded in ""YYYYMMDD format")
config = load_config()

filext = input("Enter File Type to upload (csv/mp4/avi):")
subdir = input("Enter sub-dir name :")
containername = input("Enter container name:")
connection_string = config[0]["azure_storage_connectionstring"]

if filext == "csv":
    videos = get_files(config[0]["source_folder"]+"/"+subdir)
    upload(videos, connection_string, containername,filext)
elif filext == "mp4":
    videos = get_files(config[0]["source_folder"] + "/" + subdir)
    upload(videos, connection_string, containername, filext)
elif filext == "avi":
    videos = get_files(config[0]["source_folder"] + "/" + subdir)
    upload(videos, connection_string, containername, filext)
else:
    print("not a valid extension !!")




print(f"####File upload completed at {datetime.datetime.now()}")
