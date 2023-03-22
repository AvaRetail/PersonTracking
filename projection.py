import cv2
import numpy as np

class Projection():

    '''
    
    This involves calculation of Projection matrix which is responsible for the conversion of world co-oridnates to the image co-ordinates.
    This also involves the calculation of PnP.

    '''

    def __init__(self, gps, ips, camMat, disCoeff) -> None:
        self.gps = gps
        self.ips = ips
        self.camMat = camMat
        self.disCoeff = disCoeff

    def solve(self, flag=None):
        # https://docs.opencv.org/3.4/d5/d1f/calib3d_solvePnP.html

        if flag:

            (success, rvec, tvec) = cv2.solvePnP(self.gps, self.ips, self.camMat, self.disCoeff, None, flags=cv2.SOLVEPNP_ITERATIVE)
            R = cv2.Rodrigues(rvec) # This step converts the rotation-vector (rvec) to a rotation matrix (R)

            # P = np.ones(shape=(4,4),dtype=np.float16)
            # P[:3,3] = tvec.squeeze()
            # P[3,3] = 1

            extrMat1 = np.hstack((R[0],tvec.reshape(3,1)))
            extrMat2 = np.array([0, 0, 0, 1]).reshape(1,4)
            extrMat = np.vstack((extrMat1, extrMat2))

            Psub1 = np.dot(self.camMat, np.hstack((np.eye(3,3),np.zeros((3,1)))))
            P = np.dot(Psub1, extrMat)


            return P, R, tvec

        else:

            (success, rvec, tvec) = cv2.solvePnP(self.gps, self.ips, self.camMat, self.disCoeff, None, flags=cv2.SOLVEPNP_ITERATIVE)
            R = cv2.Rodrigues(rvec) # This step converts the rotation-vector (rvec) to a rotation matrix (R)


            extrMat1 = np.hstack((R[0],tvec.reshape(3,1)))
            extrMat2 = np.array([0, 0, 0, 1]).reshape(1,4)
            extrMat = np.vstack((extrMat1, extrMat2))

            Psub1 = np.dot(self.camMat, np.hstack((np.eye(3,3),np.zeros((3,1)))))
            P = np.dot(Psub1, extrMat)


            return P, R, tvec

    def solveCamPos(self, R0, tvec):

        return np.dot(-np.transpose(R0), tvec)







