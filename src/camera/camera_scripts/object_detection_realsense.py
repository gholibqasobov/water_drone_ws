import pyrealsense2 as rs
import numpy as np
import cv2
from ultralytics import YOLO

yolo = YOLO("yolo11n.pt")


pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)


def getColours(cls_num):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = cls_num % len(base_colors)
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color = [base_colors[color_index][i] + increments[color_index][i] * 
    (cls_num // len(base_colors)) % 256 for i in range(3)]
    return tuple(color)


try:
    pipeline.start(config)
    print("Camera started. Press 'q' to quit.")

    while True:
        # Wait for frames
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        # Convert to numpy array
        if color_frame:
            color_image = np.asanyarray(color_frame.get_data())
            results = yolo.track(color_image, stream=True)

            for result in results:
                # get the classes names
                classes_names = result.names

                # iterate over each box
                for box in result.boxes:
                    # check if confidence is greater than 40 percent
                    if box.conf[0] > 0.4:
                        # get coordinates
                        [x1, y1, x2, y2] = box.xyxy[0]
                        # convert to int
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                        # get the class
                        cls = int(box.cls[0])

                        # get the class name
                        class_name = classes_names[cls]

                        # get the respective colour
                        colour = getColours(cls)

                        # draw the rectangle
                        cv2.rectangle(color_image, (x1, y1), (x2, y2), colour, 2)

                        # put the class name and confidence on the image
                        cv2.putText(color_image, f'{classes_names[int(box.cls[0])]} {box.conf[0]:.2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, colour, 2)
                    
            

            # Display the frame
            cv2.imshow('RealSense', color_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()

    # I have added this comment and printline in realsense_pose branch
    print("Hello world")
    