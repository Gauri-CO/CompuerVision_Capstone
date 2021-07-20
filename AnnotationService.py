
import cv2 as cv
import time
import yaml
import os

def object_df(filename):
    #filename = 'C://Users/gauri/PycharmProjects/ComputerVisionAnalytics/videos/VIRAT_S_000207_00_000000_000045.viratdata.objects.txt'
    valdict = {}
    with open(filename) as f:
        contents = f.readlines()

    for content in contents:
        val = list(map(int, content.strip().split(" ")))
        key = val[2]
        if val[0] == 1:
            if key in valdict.keys():
                valdict[key].append(val)
            else:
                valdict[key] = [val]

    return valdict


def video_info(cap):
    info = {}
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))  # total no of frames in the video
    fps = cap.get(cv.CAP_PROP_FPS)  # No of frames per second
    total_dur = frame_count / fps  # Total Duration of the video
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    info['frame_count'] = frame_count
    info['fps'] = fps
    info['total_dur'] = total_dur
    info['fourcc'] = fourcc
    info['frame_width'] = frame_width
    info['frame_height'] = frame_height

    return info


def modify_frames(video_name, annotationfile):
    # bounding box details#
    # start_point = (5, 5)
    # end_point = (220, 220)
    color = (255, 0, 0)
    thickness = 2

    my_video_name = video_name.split(".")[0]+".avi"
    count = 0

    cap = cv.VideoCapture(video_name)
    #print("Video name :{}".format(video_name))
    info_dict = video_info(cap)

    # Define the codec and create VideoWriter object
    fps = info_dict['fps']
    fourcc = info_dict['fourcc']
    frame_width = info_dict['frame_width']
    frame_height = info_dict['frame_height']
    frame_count = info_dict['frame_count']

    # Get Dataframe info object file
    filename = annotationfile
    df = object_df(filename)
    # print("No of rows in Person Object DataFrame: {}".format(len(df.index)))

    # out = cv.VideoWriter(my_video_name + '.avi', fourcc, fps, (frame_width, frame_height))
    out = cv.VideoWriter(my_video_name, fourcc, fps, (frame_width, frame_height))
    print(f"Processing for Video {video_name}")
    print(f"Annotation File Name {annotationfile}")
    print('Frame processing Started..')
    print('Total number of frames to be processed: {}'.format(frame_count))
    start_time = time.time()
    print('Processing ....')

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            count += 1
            cap.set(1, count)
            if count in df.keys():
                #print(f" current frame value is {count}")
                for row in df[count]:
                    start_point = (row[3], row[4])
                    end_point = (row[5] + row[3], row[6] + row[4])
                    '''print(
                        "frame no {} and end point is {} and start point is {} and color {} and thickness {} ".format(
                            count,
                            end_point,
                            start_point,
                            color,
                            thickness))'''
                    frame = cv.rectangle(frame, start_point, end_point, color, thickness)

            out.write(frame)
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv.destroyAllWindows()
    print(f"Output File {my_video_name}")
    print('Total Processing Time:---%s---' % (time.time() - start_time))
    print('Frame processing completed successfully')


def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))

    with open(dir_root + "/config.yaml", "r") as yamlfile:
        try:
            return yaml.load(yamlfile, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            print(f"Error : {e}")


if __name__ == '__main__':

    config = load_config()

    path1 = config[0]["source_folder"] + "/videos"

    for filename in os.listdir(path1):
        filepattern = filename.split(".")[0]
        video_name = path1 + "/" + filepattern + ".mp4"
        annotationfile = path1 + "/" + filepattern + ".viratdata.objects.txt"
        modify_frames(video_name, annotationfile)