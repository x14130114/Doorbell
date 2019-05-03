import subprocess
import os
from time import sleep

class AWS:

    _pid = None

    is_active = False

    def __init__(self, fb):
        self._fb = fb

    def start_stream(self):
        self.is_active = True
        self._fb.update_data({
            'doorbell/streaming/start_requested': 0
        })
        subprocess.call('nohup gst-launch-1.0 -v v4l2src device=/dev/video0 ! videoconvert ! video/x-raw,width=640,'
                        'height=480,framerate=30/1,format=I420 ! omxh264enc periodicty-idr=45 inline-header=FALSE ! '
                        'h264parse ! video/x-h264,stream-format=avc,alignment=au,profile=baseline ! kvssink name=sink '
                        'stream-name="test" access-key="AKIAIEKOVTSQMMS4JRTQ" secret-key="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" '
                        'alsasrc device=hw:2,0 ! audioconvert ! avenc_aac ! queue ! sink. >/dev/null 2>&1 &', shell=True)
        get_pid = subprocess.Popen("ps aux | pgrep gst-launch-1.0", shell=True, stdout=subprocess.PIPE).stdout
        self._pid = get_pid.read()
        print("My process id is %s" % self._pid.decode())

    def stop_stream(self):
        print('stopping')
        os.system('kill -9 %s' % self._pid.decode())
        sleep(2)
        self.is_active = False
        self._fb.update_data({
            'doorbell/streaming/stop_requested': 0
        })
