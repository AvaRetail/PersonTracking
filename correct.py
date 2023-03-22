import cv2
import numpy as np

class undistort():
    def __init__(self, intCamMat, distCoeff) -> None:
        self.distCoeff = distCoeff
        self.intCamMat = intCamMat

    def undistortImage(self, imgArr):
        h, w = imgArr.shape[:2]
        new_cam_mat, roi = cv2.getOptimalNewCameraMatrix(self.intCamMat, self.distCoeff, (w,h), 0)
        dst = cv2.undistort(imgArr, self.intCamMat, self.distCoeff, None, new_cam_mat)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        
        return dst


if __name__=="__main__":

    #Use this code to test
    dist_coeff = np.array([[-0.42799431],
    [ 0.19558802],
    [ 0.00099423],
    [-0.00064225],
    [-0.02843559]]
    )

    cam_mat = np.array([[1.82625961e+03, 0.00000000e+00, 1.25134147e+03],
    [0.00000000e+00, 1.54135456e+03, 7.05457440e+02],
    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

    img = cv2.imread(r"201.png")

    undis = undistort(cam_mat, dist_coeff)

    img = undis.undistortImage(img)
    # print(img.shape) ## Check the image shape

    # Displaying and saving the image
    # cv2.imshow("Resized_Window", img)
    cv2.imwrite("c201.png",img)
    # cv2.waitKey(0)
