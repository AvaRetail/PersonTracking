import numpy as np
from projection import Projection
from arucoDetector import arucoDetector
from correct import undistort
import cv2
from utils.operations import findIp, nameProjMat, nameCamPos, capture, imShow, mouse_click

class extrinsicCalib():

    def __init__(self, p1, p2) -> None:

        self.sq1 = self.gen_square(p1)
        self.sq2 = self.gen_square(p2)

        self.detector = arucoDetector()


    def gen_square(self, point):
        x = point[0]
        y = point[1]

        tl = np.array([x, y, 0])
        tr = np.array([x+0.15, y, 0])
        br = np.array([x+0.15, y+0.15, 0])
        bl = np.array([x,y+0.15, 0])

        return np.vstack([tl,tr,br,bl])


    def gen_ips(self, img, undist, flag=None):
        corners, ids = self.detector.arucoDetect(undist.undistortImage(img)) #imp: self.img or self.undistort_img()
        corners_list = []

        if flag:
            for i, value in enumerate(ids):
                if value == 38:
                    corners_0 = corners[i]
                    corners_list.append(corners_0.squeeze())

                if value == 62:
                    corners_5 = corners[i]
                    corners_list.append(corners_5.squeeze())

                # print(value)
      
            # cv2.imshow("img", self.detector.drawArucos(undist.undistortImage(img)))
            # # cv2.setMouseCallback("img", mouse_click)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            
            # return np.vstack([corners_0.squeeze(), corners_5.squeeze()])
            return np.vstack(corners_list)
        
        else:

            for corner in corners:
                corners_list.append(corner.squeeze())

            return np.vstack(corners_list),  ids, corners


    def gen_gps(self, img, undist, flag=None):

        if flag:
            return np.vstack([self.sq1, self.sq2])

        else:
            # ips = 
            ips = self.gen_ips(img, undist, None)[0].transpose() #to convert form nx2 to 2xn
            nps = ips.shape[1] # total no. of image points
            Ips = np.ones((3, nps)) 
            Ips[:2,:] = ips #converting 2D to homogeneous coords

            proj_mat = np.load("projMat.npy") #loading the projection matrix from the previously calculated.
            proj_mat = np.delete(proj_mat, 2, 1)

            Gps = np.dot(np.linalg.inv(proj_mat), Ips) #Calcualting all the Ips(3xn) to Gps(3xn) at the same time

            gps = Gps*1/Gps[2,:] #dividing with the homogeneous coords

            gps = np.delete(gps, 2, 0).transpose()

            support = np.zeros((nps,3), dtype=np.float32) 

            support[:,:2] = gps #converting 2D to 3D by adding z axis value as 0

            return support


    def capture(self, cam_string):

        cap = cv2.VideoCapture(cam_string)
        _, frame = cap.read()
        cap.release()

        return frame


    def primaryCalibrate(self, cam_string):

        undist = undistort(int_cam_mat1, dist_coeff1)
        img = self.capture(cam_string)
        
        gps = self.gen_gps(img, undist, 1)
        ips = self.gen_ips(img, undist ,1)
        proj = Projection(gps, ips, int_cam_mat1, np.zeros_like(dist_coeff1))  ##important: self.dist_coeff, np.zeros_like(self.dist_coeff)
           
        P, R, t = proj.solve(1)
        np.save("projMat.npy", P)

        vec = proj.solveCamPos(R[0],t)
        np.save("camPos.npy",vec)


        Gps = self.gen_gps(img, undist, None)
        Ips = self.gen_ips(img, undist, None)[0]
        Proj = Projection(Gps.astype('float32'), Ips.astype('float32'), int_cam_mat1, np.zeros_like(dist_coeff1))

        P, R, t = Proj.solve(None)

        cam1_val = findIp(cam_string)[-3:]
        np.save(nameProjMat(cam1_val), P)

        Vec = Proj.solveCamPos(R[0],t)
        np.save(nameCamPos(cam1_val),Vec)

        print(f"posn of {cam1_val} is {Vec}")


    def camera2_calibrate(self, cam_string2, cam_string1):
  
        undist1 = undistort(int_cam_mat1, dist_coeff1)
        undist2 = undistort(int_cam_mat2, dist_coeff2)

        img_arr1 = self.capture(cam_string1)
        ips1, ids1, corners1 = self.gen_ips(img_arr1, undist1)

        img_arr2 = self.capture(cam_string2)
        ips2, ids2, corners2 = self.gen_ips(img_arr2, undist2)

        ids1 = list(np.array(ids1).ravel())
        ids2 = list(np.array(ids2).ravel())

        idx1=[]
        idx2=[]

        for i, val1 in enumerate(ids1):
            if val1 in ids2:
                idx1.append(i)
                idx2.append(ids2.index(val1))

        gps1 = self.gen_gps(img_arr1, undist1)
        gps1 = gps1.reshape(len(ids1),4,3)

        gps2 = gps1[idx1].reshape(len(idx1)*4,3)
        ips2 = ips2.reshape(len(ids2),4,2)
        ips2 = ips2[idx2].reshape(len(idx2)*4,2)

        proj = Projection(gps2, ips2, int_cam_mat2, np.zeros_like(dist_coeff2))
        p, R, t = proj.solve()

        cam2_val = findIp(cam_string2)[-3:]
        np.save(nameProjMat(cam2_val), p)

        Vec = proj.solveCamPos(R[0],t)
        np.save(nameCamPos(cam2_val), Vec)

        print(f"posn of {cam2_val} is {Vec}")

def main():
    global int_cam_mat1, int_cam_mat2
    global dist_coeff1, dist_coeff2

    int_cam_mat1 = np.load("files/int_cam_mat_201.npy")
    dist_coeff1 = np.load("files/dist_coeff_201.npy")

    int_cam_mat2 = np.load("files/int_cam_mat_208.npy")
    dist_coeff2 = np.load("files/dist_coeff_208.npy")


    extrnCalib = extrinsicCalib((0.78,1.88), (1.55,2.51))
    extrnCalib.primaryCalibrate("rtsp://admin:_056pwjr@192.168.21.201")
    extrnCalib.camera2_calibrate("rtsp://admin:123456@192.168.21.208:554/stream0", "rtsp://admin:_056pwjr@192.168.21.201")

def extractWorldPos(proj_mat_path, cam_string, int_cam_mat, dist_coeff, flag=None):
    '''
    prj_mat_pat: give the path of the projection matrix of the camera of which you want extract world pose
    cam_string: give the link string of the camera
    int_cam_mat: give the intrinsic matrix of the camera
    dist_coeff: give the distortion coefficient
    flag: given flag will undistort the image of the camera for better results
    '''

    p = np.load(proj_mat_path)
    p = np.delete(p, 2, 1)

    img = capture(cam_string)
    # imShow(img)

    if flag:
        undist = undistort(int_cam_mat, dist_coeff)
        img = undist.undistortImage(img)

    arcDet = arucoDetector()
    corners, ids = arcDet.arucoDetect(img)

    corner = []
    for i, val in enumerate(ids):
        if val == 35:
            corner.append(corners[i].squeeze())

    pos = np.ones((3,), np.int16)
    pos[0] = corner[0][0, 0]
    pos[1] = corner[0][0, 1]

    world_pos = np.dot(np.linalg.inv(p), pos.reshape(3,1)).squeeze()
    world_pos = np.dot(world_pos, 1/world_pos[2])
    print(cam_string, world_pos)

def verify():
    '''
    This function is to verify the whether existing projection matrices of both the matrices are working or not.
    In order to do so place an aruco board of id = 35
    Also add verify() function in the __main__ code instead of main()
    '''

    extractWorldPos("files\projMat\projMat_201.npy", "rtsp://admin:_056pwjr@192.168.21.201", int_cam_mat1, dist_coeff1, 1)
    extractWorldPos("files\projMat\projMat_208.npy", "rtsp://admin:123456@192.168.21.208:554/stream0", int_cam_mat2, dist_coeff2, 1)

if __name__=="__main__":
    int_cam_mat1 = np.load("files/int_cam_mat_201.npy")
    dist_coeff1 = np.load("files/dist_coeff_201.npy")

    int_cam_mat2 = np.load("files/int_cam_mat_208.npy")
    dist_coeff2 = np.load("files/dist_coeff_208.npy")

    verify()
    # main()





    




