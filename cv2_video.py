import cv2
import os

class CV2Video:

    video = None
    face_detector = cv2.face.LBPHFaceRecognizer_create()
    cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')

    @staticmethod
    def capture():
        if CV2Video.video is None:
            CV2Video.video = cv2.VideoCapture(0)

    @staticmethod
    def release():
        if CV2Video.video is not None:
            CV2Video.video.release()
            CV2Video.video = None

    @staticmethod
    def convert_to_grey(picture):
        return cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)

