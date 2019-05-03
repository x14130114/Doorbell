from aws import AWS
from firebase import Firebase
from time import sleep
from new_face import NewFace


fb = Firebase()
aws = AWS(fb)
nf = NewFace(fb)


def listen():
    while True:
        data = fb.get_data()
        aws_start_requested = data['doorbell']['streaming']['start_requested']
        aws_stop_requested = data['doorbell']['streaming']['stop_requested']
        new_face_request = data['doorbell']['face']['start_new']

        # aws stream check
        if aws_start_requested == 1 and aws.is_active is False:
            aws.start_stream()

        if aws_stop_requested == 1 and aws.is_active is True:
            aws.stop_stream()

        # if new face requested
        if new_face_request == 1 and nf.is_active is False and aws.is_active is False:
            nf.take_pictures()
        else:
            fb.update_data({
                'doorbell/face/start_new': 0
            })


listen()



