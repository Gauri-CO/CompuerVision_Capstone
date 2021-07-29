# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /usr/local/src

RUN mkdir -p /usr/local/src/videos
RUN mkdir -p /usr/local/src/targetvideos
RUN mkdir -p /usr/local/src/downloads
RUN mkdir -p /usr/local/src/annotated_files
RUN mkdir -p /usr/local/src/annotated_videos
RUN mkdir -p /usr/local/src/config


COPY requirements.txt requirements.txt

RUN apt-get update -y
RUN apt install libgl1-mesa-glx -y
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install azure-storage-blob --upgrade

COPY config.yaml config.yaml
COPY yolov3.cfg /usr/local/src/config/yolov3.cfg
COPY yolov3.weights /usr/local/src/config/yolov3.weights
COPY coco.names /usr/local/src/config/coco.names
COPY AnnotationService.py AnnotationService.py
COPY LoggerFile.py LoggerFile.py
COPY Upload.py Upload.py
COPY DownloadBlob.py DownloadBlob.py
COPY Yolo.py Yolo.py
COPY AnalyticsPipeline.py AnalyticsPipeline.py
COPY VIRAT* /usr/local/src/videos/


CMD [ "python", "./AnalyticsPipeline.py" ]
