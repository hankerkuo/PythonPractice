import cv2
import numpy as np

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('C:/Users/b0050/Videos/Harrypotter/philosopher\'s stone.mp4')

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")

# Read until video is completed
num = 0
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        # save each frame
        cv2.imwrite('C:/Users/b0050/Videos/Harrypotter/capture/%d.jpg' % num, frame)

        # Display the resulting frame
        cv2.imshow('Frame', frame)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break
    num += 1
# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()