import yaml
import os
from datetime import datetime
import pathlib
import AnnotationService
import LoggerFile
import Upload
import DownloadBlob
import Yolo

log = LoggerFile.my_logger()

def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))

    with open(dir_root + "/config.yaml", "r") as yamlfile:
        try:
            return yaml.load(yamlfile, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            print(e)


class createYML:

    def __init__(self, path):
        self.path = path

    def writeyaml(self):
        info = [
            {

                'azure_storage_connectionstring': "DefaultEndpointsProtocol=https;AccountName=retailanalytics08;AccountKey=Vk+/9Z9quDj3p1cY1AIaZ4GrCr+bNgU7JnknY9DpuWlF6o31jWo6wrOSU3rciJs4sxQ0+M8dItaTrhhCgGsJzQ==;EndpointSuffix=core.windows.net",
                'video_container_name': 'videos',
                'source_folder': self.path,
                'annotatedfiles': 'annotatedfiles',
                'mp4_file_pattern': '^VIRAT[_]S[_]\d{6}[_]\d{2}[_]\d{6}[_]\d{6}[_]\d{8}[\.]mp4$',
                'csv_file_pattern': '^VIRAT[_]S[_]\d{6}[_]\d{2}[_]\d{6}[_]\d{6}[_]\d{8}[\.]csv$',
                'avi_file_pattern': '^VIRAT[_]S[_]\d{6}[_]\d{2}[_]\d{6}[_]\d{6}[_]\d{8}[\.]avi$'

            }
        ]

        with open("config.yaml", 'w') as yamlfile:
            data = yaml.dump(info, yamlfile)
            print("Write successful")


class addTimestamp:

    def __init__(self, config):
        self.config = config

    def updatetimestamp(self):
        path1 = self.config[0]["source_folder"] + "/videos"
        path2 = self.config[0]["source_folder"] + "/targetvideos"
        for filename in os.listdir(path1):
            filext = filename.split(".")[-1]
            if filext == "mp4":
                name = filename.replace('.mp4', '')
                date = datetime.now().strftime("%Y%m%d")
                newfilename = name + "_" + date + ".mp4"
                print(f"{newfilename}")
                p1 = pathlib.PureWindowsPath(path1)
                p2 = pathlib.PureWindowsPath(path2)

                cmd = f"copy {p1}\{filename} {p2}\{newfilename}"
                print(f"Running ....{cmd}")
                os.system(cmd)


if __name__ == "__main__":


    print("#####Retail Analytics Application######")
    path = input("Enter the path for video files:")

    log.info("---YAML file creation Started---")
    cy = createYML(path.strip())
    cy.writeyaml()
    config = load_config()
    log.info("---YAML file creation completed---")

    log.info("---Timestamp Update Started---")
    addTimestamp(config).updatetimestamp()
    log.info("---Timestamp Update completed---")

    path1 = config[0]["source_folder"] + "/videos"

    log.info("---Annotation Service Started---")
    for filename in os.listdir(path1):
        filepattern = filename.split(".")[0]
        video_name = path1 + "/" + filepattern + ".mp4"
        annotationfile = path1 + "/" + filepattern + ".viratdata.objects.txt"
        AnnotationService.modify_frames(video_name, annotationfile)
    log.info("---Annotation Service Completed---")

    log.info("---Upload Service Started---")
    connection_string=config[0]["azure_storage_connectionstring"]
    videos = Upload.get_files(config[0]["source_folder"] + "/targetvideos")
    Upload.upload(videos, connection_string, "videos", "mp4")
    log.info("---Upload Service Completed---")


    MY_CONNECTION_STRING = config[0]["azure_storage_connectionstring"]
    MY_BLOB_CONTAINER = config[0]["video_container_name"]
    LOCAL_BLOB_PATH = config[0]["source_folder"] + "/downloads/"

    log.info("---Download Service Started---")
    azure_blob_file_downloader = DownloadBlob.AzureBlobFileDownloader(MY_CONNECTION_STRING,MY_BLOB_CONTAINER,LOCAL_BLOB_PATH)
    azure_blob_file_downloader.download_all_blobs_in_container()
    log.info("---Download Service Completed---")

    log.info("---Yolo Annotation service Started--")
    Yolo.runyolo()
    log.info("---Yolo Annotation service Completed--")

    log.info("---Final File upload to Azure Blob Started---")
    annotatedvideos = Upload.get_files(config[0]["source_folder"] + "/annotated_videos")
    Upload.upload(annotatedvideos, connection_string, "annotatedvideos", "avi")

    annotatedvideos = Upload.get_files(config[0]["source_folder"] + "/annotated_files")
    Upload.upload(annotatedvideos, connection_string, "annotatedfiles", "csv")

    log.info("---Final File upload to Azure Blob Completed---")







