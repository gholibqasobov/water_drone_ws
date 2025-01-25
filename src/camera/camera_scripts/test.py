import cv2

cam = cv2.VideoCapture(0)  # 4, 2



while True:
    ret, frame = cam.read()

    # Display the captured frame
    cv2.imshow('Camera', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cam.release()

cv2.destroyAllWindows()