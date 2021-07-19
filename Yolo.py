import cv2
import numpy as np
import argparse
import pandas as pd
import datetime
import os
import yaml
import re

ct = str(datetime.datetime.now())


def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))

    with open(dir_root + "/config.yaml", "r") as yamlfile:
        try:
            return yaml.load(yamlfile, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            print(e)


config = load_config()
path = config[0]['source_folder']
master_file = path + "/annotated_files/" + "master_file.csv"

f = open(master_file, "w+")


def check_file(filename):
    x = re.search("^VIRAT[_]S[_]\d{6}[_]\d{2}[_]\d{6}[_]\d{6}[_]\d{8}[\.]mp4$", filename, re.IGNORECASE)
    if x:
        return True
    else:
        return False


def get_files(dir):
    file_list = []
    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.is_file() and not entry.name.startswith(".") and check_file(entry.name):
                file_list.append(entry.name)

    return file_list


parser = argparse.ArgumentParser()
parser.add_argument('--webcam', help="True/False", default=False)
parser.add_argument('--play_video', help="True/False", default=True)
parser.add_argument('--image', help="Tue/False", default=False)
parser.add_argument('--video_path', help="Path of video file",
                    default=config[0]['source_folder'] + "/downloads")
parser.add_argument('--image_path', help="Path of image to detect objects",
                    default="C://Users/gauri/OpenEndedCapstoneProject/bicycle.jpg")
parser.add_argument('--verbose', help="To print statements", default=True)
args = parser.parse_args()


# Load yolo
def load_yolo():
    net = cv2.dnn.readNet(path + "/config/yolov3.weights",
                          path + "/config/yolov3.cfg")
    classes = []
    with open(path + "/config/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layers_names = net.getLayerNames()
    output_layers = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    return net, classes, colors, output_layers


def load_image(img_path):
    # image loading
    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape
    return img, height, width, channels


def start_webcam():
    cap = cv2.VideoCapture(0)

    return cap


def display_blob(blob):
    '''
        Three images each for RED, GREEN, BLUE channel
    '''
    for b in blob:
        for n, imgb in enumerate(b):
            cv2.imshow(str(n), imgb)


def detect_objects(img, net, outputLayers):
    blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(outputLayers)
    return blob, outputs


def get_box_dimensions(outputs, height, width):
    boxes = []
    confs = []
    class_ids = []
    for output in outputs:
        for detect in output:
            scores = detect[5:]
            class_id = np.argmax(scores)
            conf = scores[class_id]
            if conf > 0.3:
                center_x = int(detect[0] * width)
                center_y = int(detect[1] * height)
                w = int(detect[2] * width)
                h = int(detect[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confs.append(float(conf))
                class_ids.append(class_id)
    return boxes, confs, class_ids


def draw_labels(boxes, confs, colors, class_ids, classes, img, annotated_video_file, videodate):
    indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    annotation_tuple = ()

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])

            if label == "person":
                color = colors[i]
                annotation_tuple = (x, y, x + w, y + h, label, annotated_video_file, ct, videodate)
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y - 5), font, 1, color, 1)

    # cv2.imshow("Image", img)
    return annotation_tuple


def image_detect(img_path):
    model, classes, colors, output_layers = load_yolo()
    image, height, width, channels = load_image(img_path)
    blob, outputs = detect_objects(image, model, output_layers)
    boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
    draw_labels(boxes, confs, colors, class_ids, classes, image)

    while True:
        key = cv2.waitKey(1)
        if key == 27:
            break


def webcam_detect():
    model, classes, colors, output_layers = load_yolo()
    cap = start_webcam()
    while True:
        _, frame = cap.read()
        height, width, channels = frame.shape
        blob, outputs = detect_objects(frame, model, output_layers)
        boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
        draw_labels(boxes, confs, colors, class_ids, classes, frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()


def start_video(video_file):
    model, classes, colors, output_layers = load_yolo()
    print("--Yolo Loading Completed!!")
    cap = cv2.VideoCapture(video_file)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    annotated_video_file = video_file.split("/")[-1].split(".")[0]
    videodate = video_file.split("/")[-1].split(".")[0].split("_")[-1]
    annotated_video = path + "/annotated_videos/" + annotated_video_file + ".avi"
    # annotated_video = "C://Users/gauri/OpenEndedCapstoneProject/Annotated_Eshaan.avi"
    out = cv2.VideoWriter(annotated_video, fourcc, fps, (frame_width, frame_height))
    annotation_list = []

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        height, width, channels = frame.shape
        blob, outputs = detect_objects(frame, model, output_layers)
        boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
        # draw_labels(boxes, confs, colors, class_ids, classes, frame)
        annotation_list.append(
            draw_labels(boxes, confs, colors, class_ids, classes, frame, annotated_video_file, videodate))

        out.write(frame)

    cap.release()

    return annotation_list


if __name__ == '__main__':
    webcam = args.webcam
    video_play = args.play_video
    image = args.image
    if webcam:
        if args.verbose:
            print('---- Starting Web Cam object detection ----')
        webcam_detect()
    if video_play:
        video_path = args.video_path

        if args.verbose:
            print('--Start Time--  ' + str(datetime.datetime.now()))
            # start_video(video_path)
            video_files = get_files(path + "/downloads")
            print(video_files)
            print(f"Total no of videos to be processed {len(video_files)}")
            for video_file in video_files:
                print('Opening Video ' + video_file + " .... ")

                df = pd.DataFrame(start_video(path + "/downloads/" + video_file),
                                  columns=['center_x', 'center_y', 'width', 'height', 'label', 'filename',
                                           'current_time', 'videodate'])
                ext = video_file.split(".")[1]
                annotated_csv = video_file.replace(ext, "csv")

                if os.path.exists(path + "/annotated_files/" + annotated_csv):
                    os.remove(path + "/annotated_files/" + annotated_csv)

                df.to_csv(path + "/annotated_files/" + annotated_csv, index=False)

                if not df.empty:
                    f.write(annotated_csv + "\n")

                os.remove(path + "/downloads/" + video_file)
                # type(df)
                # print(df.head())
            f.close()
            print('--End Time-- ' + str(datetime.datetime.now()))
    if image:
        image_path = args.image_path
        if args.verbose:
            print("Opening " + image_path + " .... ")
        image_detect(image_path)

    cv2.destroyAllWindows()
