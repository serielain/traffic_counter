from ultralytics import YOLO
from ultralytics.solutions import object_counter
from datetime import datetime
import torch
import time
import sys
import cv2
import os

from create_graph import make_graph
from create_graph import make_class_wise_graph
from create_graph import create_video_from_images

#THESE ARE VARIABLES YOU NEED TO CHANGE ACCORDING TO YOUR NEEDS // THIS PROGRAM USES PYTHON 3.10.6 and YOLOV8
##############################################################################
video_source = "http://192.168.178.20:8080/video"                              # Video source (URL or path to video file)
output_dir = f"Y:/local_programming/everything_everywhere/car_counter_output"   # Output directory for saving the images
line_points = [(200, 720), (640,360)]                                          # Line points for counting objects
classes_to_track = [2,3,5,7]                                                   # Classes to track (based on YOLOv8 classes)
##############################################################################

# Create the output directory folder for each new run
folder_time = datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
os.mkdir(output_dir + f"/{folder_time}")
output_dir = os.path.join(output_dir, folder_time)

model = YOLO("yolov8n.pt")

#check if cuda is available (GPU is available with CUDA support)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)
print("Model loaded successfully.")

frame_counter = 0
frames = []

# Open the video capture
while True:
    try:
        cap = cv2.VideoCapture(video_source)
        assert cap.isOpened(), "Error reading video file"
        break  # If the video capture was opened successfully, break the loop
    except AssertionError:
        print("Failed to open video capture. Retrying...")
        time.sleep(0.1)

# Get video information
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Initialize the object counter
counter = object_counter.ObjectCounter()
counter.set_args(view_img=True,
                 reg_pts=line_points,
                 classes_names=model.names,
                 draw_tracks=True,
                 track_thickness=0,
                 region_thickness=0,
                 line_thickness=2)
total_object_count_list = []
try:
    while cap.isOpened():
        success, im0 = cap.read()

        frame_counter += 1
        if frame_counter % 30 == 0:
            frames.append(im0)

        if not success:
            print("Video frame is empty or video processing has been successfully completed.")
            break
        
        tracks = model.track(im0, persist=True, conf=0.25, show=False,verbose=False, classes=classes_to_track, tracker="bytetrack.yaml", save=False, save_crop=False)
        im0 = counter.start_counting(im0, tracks)
        total_object_count = counter.in_counts + counter.out_counts
        with open(f"{output_dir}/object_count.txt", "a") as f:
            if(total_object_count not in total_object_count_list):
                # Write the total object count to the file
                now = datetime.now()
                formatted_now = now.strftime("%d_%m_%Y__%H_%M_%S")
                f.write("\n Total Objects passed: " + str(total_object_count) + " at " + formatted_now)
                total_object_count_list.append(total_object_count)
                print("Total Objects passed (live count): ", counter.in_counts + counter.out_counts, " at ", now.strftime("%d_%m_%Y %H:%M:%S"))
                # Save the image of the frame
                image_path = os.path.join(output_dir, f'frame_{counter.in_counts + counter.out_counts}_{formatted_now}.png')
                cv2.imwrite(image_path, im0)

                with open(f"{output_dir}/class_wise_object_count.txt", "a") as f_class_wise:
                    f_class_wise.write("\n" + formatted_now +"OBJECTS"+ str(counter.class_wise_count))

    make_graph(f"{output_dir}/object_count.txt")
    make_class_wise_graph(f"{output_dir}/class_wise_object_count.txt")
except KeyboardInterrupt as e:
    print("Video processing has been interrupted by the user.")
except Exception as e:
    print(str(e) + " Error occurred while processing the video.")
finally:
    cap.release()
    cv2.destroyAllWindows()
    make_graph(f"{output_dir}/object_count.txt")
    make_class_wise_graph(f"{output_dir}/class_wise_object_count.txt")
    timelapse = input("Do you want to save a timelapse of the videostream? Y/N:  ")
    if timelapse == "Y" or timelapse == "y":
        create_video_from_images(frames, f"{output_dir}/video.mp4")