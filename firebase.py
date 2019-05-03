"""
Firebase
"""

# imports
import json
import pyrebase
import urllib
from datetime import datetime

class Firebase:
    # Firebase DB config
    _config = {
        "apiKey": "AIzaSyDCEyXXaD5dVS6DjZs7iD81xoXLVXyE8N0",
        "authDomain": "doorbell-4f1e8.firebaseapp.com",
        "databaseURL": "https://doorbell-4f1e8.firebaseio.com/",
        "projectId": "doorbell-4f1e8",
        "storageBucket": "doorbell-4f1e8.appspot.com",
        "messagingSenderId": "60290141949",
        "serviceAccount": "/home/pi/PyCharms/DoorFinal/key.json"
    }

    # login credentials as private access vars
    _login = "EMAIL"
    _password = "PASSWORD"

    # update data method
    def update_data(self, data):
        self._db.update(data)

    # get data method
    def get_data(self):
        return self._db.get().val()

    # create user with the firebase credentialsss
    def create_user(self, email, password):
        self._auth.create_user_with_email_and_password(email, password)

    """def get_storage(self):
        print("IN STORAGE!!")
        print(self._storage.child("https://firebasestorage.googleapis.com/v0/b/doorbell-4f1e8.appspot.com/o/SampleAudio_0.4mb.mp3?alt=media&token=f4a230e3-a053-48c9-aba5-323929f436dc").download("audio"))
        return self._storage.child("SampleAudio_0.4mb.mp3").download("audio")"""

    def download_file(self):
        print("IN DOWNLOAD")
        my_url = "https://firebasestorage.googleapis.com/v0/b/doorbell-4f1e8.appspot.com/o/Audio%2Fnew7.mp3?alt=media&token=63a1a73a-138a-4741-bcbe-8bf9a316936c"

        try:
            loader = urllib.request.urlretrieve(my_url, "audio.mp3")
        except urllib.error.URLError as e:
            message = json.loads(e.read())
            print(message["error"]["message"])
        else:
            print(loader)

    # Constructor method
    def __init__(self):
        # initialize firebase instance
        self._firebase = pyrebase.initialize_app(self._config)
        self._auth = self._firebase.auth()
        self._user = self._auth.sign_in_with_email_and_password(self._login, self._password)
        self._db = self._firebase.database()
        self._storage = self._firebase.storage()
