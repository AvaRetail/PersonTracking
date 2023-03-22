import re
import cv2
import contextlib
import time
from time import perf_counter

def findIp(camString):

    '''
        camstring: "rtsp://admin:_056pwjr@192.168.21.201"

        returns '192.168.21.201'
    '''

    pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')

    matches = pattern.findall(camString)

    return matches[0]

def nameProjMat(camVal):
    return r'D:\\Chetan\\Documents\\python_scripts\\smoothShop\\files\\projMat\\projMat_'+camVal+'.npy'

def nameCamPos(camVal):
    return r'D:\\Chetan\\Documents\\python_scripts\\smoothShop\\files\\camMat\\camPos_'+camVal+'.npy'

def capture(cam_string):

    cap = cv2.VideoCapture(cam_string)
    _, frame = cap.read()
    cap.release()

    return frame

def mouse_click(event, x, y,
            flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)

def imShow(img_arr, flag=None):
    '''
    img_arr: nump array which you want to show
    lst: [fx, fy] the parameters of the resize
    '''
    if flag:
        img_arr = cv2.resize(img_arr, (0,0), fx=0.5, fy=0.5)

    cv2.imshow("image", img_arr)
    cv2.setMouseCallback('image', mouse_click)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

class Profile(contextlib.ContextDecorator):
# Usage: @Profile() decorator or 'with Profile():' context manager
    def __enter__(self):
        self.start = time.time()

    def __exit__(self, type, value, traceback):
        print(f'Profile results: {time.time() - self.start:.5f}s')