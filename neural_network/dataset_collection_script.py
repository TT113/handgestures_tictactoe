import cv2
import os
import sys
import time
import neural_network.constants as constants

try:
    num_of_images = int(sys.argv[1])
    image_label = sys.argv[2]
except:
    pass

font = cv2.FONT_HERSHEY_PLAIN
click = False

label_name = os.path.join(constants.TRAINING_IMAGES_FOLDER, image_label)
count = image_name = 0
try:
    os.mkdir(constants.TRAINING_IMAGES_FOLDER)
except FileExistsError:
    pass

try:
    os.mkdir(label_name)
except FileExistsError:
    image_name = len(os.listdir(label_name))

video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 2000)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)

time_skip = 0.5
previous_time = time.time()
while True:
    ret, image = video.read()
    image = cv2.flip(image, 1)
    if not ret:
        continue
    if count == num_of_images:
        break
    cv2.rectangle(image, (200, 200), (550, 550), (255, 255, 255), 2)
    if click and time.time() - previous_time >= time_skip:
        region_of_interest = image[200:550, 200:550]
        save_path = os.path.join(label_name, '{}.jpg'.format(image_name + 1))
        cv2.imwrite(save_path, region_of_interest)
        image_name += 1
        count += 1
        previous_time = time.time()
    cv2.putText(image, "Image Count: {}".format(count),
                (20, 100), font, 1, (12, 20, 200), 2, cv2.LINE_AA)
    cv2.imshow("Get dataset", image)
    k = cv2.waitKey(10)
    if k == ord('s'):
        click = not click
video.release()
cv2.destroyAllWindows()
