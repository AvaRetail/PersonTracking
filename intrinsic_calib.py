import numpy as np
import cv2
import glob
import os
from tqdm import tqdm

class intrinsics():
    '''
    arDict - cv2.aruco.DICT_4X4_1000
    boardSize  (10, 15)
    markSize (0.025, 0.019) or (0.04, 0.03)
    '''
    def __init__(self, arDict, boardSize, markSize) -> None:
        self.chDict = cv2.aruco.getPredefinedDictionary(arDict)
        self.chBoard = cv2.aruco.CharucoBoard(boardSize, markSize[0], markSize[1], self.chDict)
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # self.flags =(cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)

    def intCalib(self, imgDir):
        cornersArr = []
        idsArr = []
        
        for img in tqdm(os.listdir(imgDir)):
            img = cv2.imread(os.path.join(imgDir,img))
            img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            (corners, ids, rej) = cv2.aruco.detectMarkers(img, self.chDict)
            res = cv2.aruco.interpolateCornersCharuco(corners, ids, img, self.chBoard)
            cornersArr.append(res[1])
            idsArr.append(res[2])
            shape = img.shape
            

        ret, mtx, dist, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(cornersArr, idsArr, self.chBoard, (int(shape[1]),int(shape[0])), None, self.criteria)

        return (ret, mtx, dist)

def main():
    intr = intrinsics(cv2.aruco.DICT_4X4_1000, (10, 15), (0.025, 0.019))
    res = intr.intCalib(r"D:\\Chetan\\Documents\\python_scripts\sarun\\201_new")

    print(">error")
    print(res[0])

    print(">camera matrix")
    print(np.array2string(res[1], separator=', '))

    print(">distortion coeff")
    print(np.array2string(res[2], separator=', '))

if __name__=="__main__":
    main()

