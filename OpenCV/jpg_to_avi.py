import cv2
import os

class config:
    def __init__(self, no_of_pictures, frame_rate, folder_of_picture, file_name):
        self.no_of_pictures = no_of_pictures
        self.frame_rate = frame_rate
        self.folder_of_picture = folder_of_picture
        self.file_name = file_name

# just modify this part, set the proper configs
# file_name is special, %d part means the different part between
# each pictures, please set %d = 0 for the first picture
# or you can modify the code to satisfy your own naming policy
custom = config(no_of_pictures=91,
                frame_rate=23,
                folder_of_picture='C:/data/moviecapture/cut3',
                file_name='%d_refined.jpg')

image_folder = custom.folder_of_picture
video_name = os.path.join(image_folder, 'video.avi')

image_0 = os.path.join(image_folder, custom.file_name % 0)
frame = cv2.imread(os.path.join(image_folder, image_0))
height, width, layers = frame.shape

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
video = cv2.VideoWriter(video_name, fourcc, custom.frame_rate, (width, height))

for no_of_image in range(custom.no_of_pictures):
    video.write(cv2.imread(os.path.join(image_folder, custom.file_name % no_of_image)))

cv2.destroyAllWindows()
video.release()