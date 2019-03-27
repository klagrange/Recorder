import os
import uuid
import time
from argparse import ArgumentParser, ArgumentTypeError
import mss
import cv2

class Monitor():

    def __init__(self, seconds: int, video: str):
        self.seconds = seconds
        self.video = video
        self.filename = "/tmp/{0}.png".format(uuid.uuid1)

    def run(self):
        imgs = []
        i = 0
        timeout = time.time() + self.seconds

        while True:    
            time_now = time.time()
            if time_now > timeout:
                break

            with mss.mss() as sct:
                i += 1
                sct.shot(output=self.filename)
                
            img = cv2.imread(self.filename)
            height, width, _ = img.shape
            size = (width, height)
            imgs.append(img)
            os.remove(self.filename)

        out = cv2.VideoWriter(self.video, cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
        for img in imgs:
            out.write(img)
        out.release()

def valid_int(number):
    return int(number)

def args():
    args = ArgumentParser()
    args.add_argument('-t', '--time', help='time of recording in seconds',
                      dest='seconds', default=5, type=valid_int)
    args.add_argument('--video', help='Override default video name',
                      dest='video', default='project.avi')
    return args.parse_args()

if __name__ == "__main__":
    arguments = args()
    monitor = Monitor(arguments.seconds, arguments.video)
    monitor.run()
