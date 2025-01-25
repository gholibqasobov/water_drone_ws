import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)

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

            # Display the frame
            cv2.imshow('RealSense', color_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()