import os
from time import sleep
import random
from cv2_video import CV2Video
import cv2
import numpy as np
from PIL import Image


class NewFace:

    is_active = False

    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    _images_dir = os.path.join(_BASE_DIR, "user")

    def __init__(self, fb):
        self._fb = fb

    def train_faces(self):
        faces = []  # an empty array for faces numeric arrays
        ids = []  # an empty array for user's id

        # walk through images in /user folder
        for root, dirs, images in os.walk(self._images_dir):
            for img in images:
                # if img has .jpg extension
                if img.endswith("jpg"):

                    face_id = int(os.path.basename(root))  # getting face_id out of the folder name
                    path = os.path.join(root, img)  # getting the path out of the picture number and root folder
                    grey_img = Image.open(path).convert('L')  # converts image to gray
                    img_arr = np.array(grey_img, 'uint8')  # creating numpy array out of the picture

                    # takes currently loaded image and detects face on it.
                    temp = CV2Video.cascade.detectMultiScale(img_arr)
                    for (x, y, w, h) in temp:
                        faces.append(img_arr[y:y + h, x:x + w])  # append face's array to faces array
                        ids.append(face_id)  # appends id to an ids array

        CV2Video.face_detector.train(faces, np.array(ids))  # run's and train algorithm with detector instructions
        CV2Video.face_detector.save('trainer.yml')  # saves yml output
        print("COMPLETE")

    def take_pictures(self):
        self.is_active = True
        CV2Video.capture()
        # time countdown before take the picture (5s)
        ct = 5
        while ct > 0:
            print('Please look at the camera now. We will take a few pictures in: %s' % ct)
            sleep(1)
            ct = ct - 1
            os.system('clear')

        # check if folder already exists
        if os.path.exists('user') is False:
            os.mkdir('user')

        # get random id and if exists re-randomize again
        user_id = random.SystemRandom().randint(10000, 99999)
        while True:
            if os.path.exists('user/%s' % user_id) is False:
                os.mkdir('user/%s' % user_id)
                break
            else:
                user_id = random.SystemRandom().randint(10000, 99999)

        counter = 0  # will count pictures which were taken

        # taking user's pictures
        while True:
            ret, frame = CV2Video.video.read()  # ret - bool, frame - current camera frame
            gray = CV2Video.convert_to_grey(frame)  # convert picture to greyscale
            faces = CV2Video.cascade.detectMultiScale(gray, 1.5, 5)  # detect faces

            # iterate through detected
            for (x, y, w, h) in faces:
                cv2.imwrite("user/%s/%s.jpg" % (user_id, counter), gray[y: y + h, x: x + w])
                counter = counter + 1

            if counter == 40:  # at the 10th picture stop
                self.train_faces()  # run train algorithm

                # print successful message
                print('Your profile was created! Thanks!')
                self.is_active = False
                CV2Video.release()
                self._fb.update_data({
                    'doorbell/face/start_new': 0
                })
                break
