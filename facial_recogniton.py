import cv2_video
import os
import numpy as np
from PIL import Image
from self import self

class FacialRecognition:

    # constant private variables
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    _images_dir = os.path.join(_BASE_DIR, "user")

    # indicator if registration is going on
    is_registration_on = False

    # bool value returned in relation to check if trained faces file exists.
    @staticmethod
    def trainer_exists():

        return os.path.exists('trainer.yml')

    # loads .yml file of trainer
    def load_trainer(self):

        self.face_detector.read('trainer.yml')

    # constructor class
    def __init__(self):

        #self.video = cv2.VideoCapture(0) # capture video from source '0' - raspi camera
        # load face detection instructions - Created by Rainer Lienhart.
        self.cascade = cv2_video.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
        self.face_detector = cv2_video.face.LBPHFaceRecognizer_create() # creates face recognizer
        if self.trainer_exists(): # checks if trainer.yml exists
            self.load_trainer()

    # convert's picture to grey using open cv method
    @staticmethod
    def convert_to_grey(picture):

        return cv2_video.cvtColor(picture, cv2_video.COLOR_BGR2GRAY)

    # method which is looping recognising face front of the camera.
    def recognize(self):
        #print("TEST")
        # ret - return boolean and frame is the current frame captured from the camera
        self.video = cv2_video.VideoCapture(0)
        ret, frame = self.video.read()
        gray = self.convert_to_grey(frame)
        # detect faces through the cascade instructions
        faces = self.cascade.detectMultiScale(gray, 1.3, 5)

        # iterating through found objects
        for (x, y, w, h) in faces:
            # if user_id was associated with the face set active user
            face_id, score = self.face_detector.predict(gray[y: y + h, x: x + w])
            return (face_id, score)

    # train faces method
    def train_faces(self):

        faces = [] # an empty array for faces numeric arrays
        ids = [] # an empty array for user's id

        # walk through images in /user folder
        for root, dirs, images in os.walk(self._images_dir):
            for img in images:
                # if img has .jpg extension
                if img.endswith("jpg"):

                    face_id = int(os.path.basename(root)) # getting face_id out of the folder name
                    path = os.path.join(root, img) # getting the path out of the picture number and root folder
                    grey_img = Image.open(path).convert('L') # converts image to gray
                    img_arr = np.array(grey_img, 'uint8') # creating numpy array out of the picture

                    # takes currently loaded image and detects face on it.
                    temp = self.cascade.detectMultiScale(img_arr)
                    for (x, y, w, h) in temp:
                        faces.append(img_arr[y:y + h, x:x + w]) # append face's array to faces array
                        ids.append(face_id) # appends id to an ids array

        self.face_detector.train(faces, np.array(ids)) # run's and train algorithm with detector instructions
        self.face_detector.save('trainer.yml')  # saves yml output
        print("COMPLETE")

#FacialRecognition.train_faces()
