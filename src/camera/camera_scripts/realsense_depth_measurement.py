import pyrealsense2 as rs
import numpy as np

# Create a pipeline
pipeline = rs.pipeline()

# Configure the pipeline to enable the depth stream
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

try:
    # Start the pipeline
    pipeline.start(config)
    print("Depth camera started. Press Ctrl+C to stop.")

    while True:
        # Wait for frames
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        if depth_frame:
            # Get the depth value at the center of the frame
            width = depth_frame.get_width()
            height = depth_frame.get_height()
            center_x, center_y = width // 2, height // 2

            # Retrieve depth value at the center
            depth_value = depth_frame.get_distance(center_x, center_y)  # In meters

            print(f"Depth at center ({center_x}, {center_y}): {depth_value:.3f} meters")

except KeyboardInterrupt:
    print("\nStopping depth camera...")

finally:
    # Stop the pipeline
    pipeline.stop()
    print("Camera stopped.")