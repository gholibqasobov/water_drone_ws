import pyrealsense2 as rs

# Create a pipeline
pipeline = rs.pipeline()

# Create a config and enable the default stream
config = rs.config()
try:
    # Enable a supported color stream (e.g., 640x480 resolution at 30fps)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
    
    # Start the pipeline
    profile = pipeline.start(config)
    print("Pipeline started successfully!")
    
    # Wait for a frame
    frames = pipeline.wait_for_frames(10000)
    print("Frames received!")
    
except RuntimeError as e:
    print(f"RuntimeError: {e}")

finally:
    pipeline.stop()