import numpy as np
from queue import Queue
from argparse import ArgumentParser, ArgumentTypeError
import time
import cv2

class Webcam:
    
    def __init__(self, seconds: int = 10):
        self.seconds = seconds

    def run(self):
        cap = cv2.VideoCapture(0)
        timeout = time.time() + self.seconds

        while True:    
            time_now = time.time()
            if time_now > timeout:
                break

            # capture frame-by-frame
            _, frame = cap.read()

            # our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # display the resulting frame
            cv2.imshow('frame', gray)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # when everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

def valid_int(number):
    return int(number)

def args():
    args = ArgumentParser()
    args.add_argument('-t', '--time', help='time of recording in seconds',
                      dest='seconds', default=5, type=valid_int)
    return args.parse_args()

if __name__ == "__main__":
    arguments = args()
    webcam = Webcam(arguments.seconds)
    webcam.run()
