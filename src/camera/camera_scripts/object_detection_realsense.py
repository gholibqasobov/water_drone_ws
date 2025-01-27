import pyrealsense2 as rs
import numpy as np
import cv2
import math
from ultralytics import YOLO
from timeit import default_timer as timer
from PIL import Image
from decimal import Decimal, ROUND_HALF_UP

yolo = YOLO("yolo11n.pt")

pipeline = rs.pipeline()
align_to = rs.stream.color

config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

def getColours(cls_num):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = cls_num % len(base_colors)
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color = [base_colors[color_index][i] + increments[color_index][i] *
             (cls_num // len(base_colors)) % 256 for i in range(3)]
    return tuple(color)

def calculate_real_world_coordinates(depth_frame, center_coordinates, intr, theta):
    X, Y, Z = [], [], []
    for coord in center_coordinates:
        dist = depth_frame.get_distance(int(coord[0]), int(coord[1])) * 1000  # Convert to mm
        Xtemp = dist * (coord[0] - intr.ppx) / intr.fx
        Ytemp = dist * (coord[1] - intr.ppy) / intr.fy
        Ztemp = dist

        Xtarget = Xtemp - 35  # Adjust for the camera offset
        Ytarget = -(Ztemp * math.sin(theta) + Ytemp * math.cos(theta))
        Ztarget = Ztemp * math.cos(theta) + Ytemp * math.sin(theta)

        X.append(Xtarget)
        Y.append(Ytarget)
        Z.append(Ztarget)
    return X, Y, Z

try:
    profile = pipeline.start(config)
    align = rs.align(align_to)
    intr = profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()

    theta = 0  # Define rotation angle for pose calculations
    print("Camera started. Press 'q' to quit.")

    while True:
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()

        if not color_frame or not depth_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())
        results = yolo.track(color_image, stream=True)
        center_coordinates = []

        for result in results:
            classes_names = result.names

            for box in result.boxes:
                if box.conf[0] > 0.4:
                    [x1, y1, x2, y2] = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cls = int(box.cls[0])
                    class_name = classes_names[cls]
                    colour = getColours(cls)
                    cv2.rectangle(color_image, (x1, y1), (x2, y2), colour, 2)
                    cv2.putText(color_image, f'{class_name} {box.conf[0]:.2f}', 
                                (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, colour, 2)
                    
                    # Calculate center of the box
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    center_coordinates.append((cx, cy))

        if center_coordinates:
            X, Y, Z = calculate_real_world_coordinates(depth_frame, center_coordinates, intr, theta)

            for i, (cx, cy) in enumerate(center_coordinates):
                coordinates_text = f"({Decimal(X[i]).quantize(Decimal('0'), rounding=ROUND_HALF_UP)}, " \
                                   f"{Decimal(Y[i]).quantize(Decimal('0'), rounding=ROUND_HALF_UP)}, " \
                                   f"{Decimal(Z[i]).quantize(Decimal('0'), rounding=ROUND_HALF_UP)})"
                cv2.putText(color_image, coordinates_text, (cx - 160, cy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Display the frame
        cv2.imshow('RealSense', color_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
    print("Camera stopped.")
