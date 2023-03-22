
import cv2
import numpy as np
import os
from ast import literal_eval

from merging import shopper
# def instanceCheck(data):
#     retnval = True
#     for i in data:
#         retnval = retnval or isinstance(i, np.ndarray)

#     return retnval

def instanceCheck(data):

    retnval = isinstance(data[0], np.ndarray) or isinstance(data[1], np.ndarray)

    return retnval

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def drawShoppers(camMapClone, shoppers: list[shopper]):

    for shopper in shoppers:
        print(f"The position of shopper-{shopper.id} X is {shopper.x}, Y is {shopper.y} id is {shopper.id}, and storage: device is {shopper.storage}: {shopper.device}")
        
        cv2.circle(camMapClone, (int(shopper.x), int(shopper.y)), 10, (0, 255, 0), 2)
        cv2.putText(camMapClone, f'id_{shopper.id}', (int(shopper.x), int(shopper.y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    return camMapClone

def operation(msg, proj_mat):

    op = msg.payload.decode().replace(' ','').replace('[','').replace(']','').rsplit(",")

    try: 
        op = list(map(eval, op)) # converts the string into list of floating numbers

        nPers = len(op)//516
        op = np.array(op).reshape((nPers,516)) # 516 [x, y, id, device_id, feature of len 512]

        track = list(op[:,:3].ravel())
        device_id = op[:,3]
        features = op[:, 4:]
        iter_op = iter(track) #converts the list into iterable object

        persPos = np.ones((nPers, 3), np.int16) #creating a numpy array to store the person positions
        tracker = np.ones((nPers, 516))

        for i in range(nPers):
            persPos[i,:2] = np.array([int(next(iter_op)), int(next(iter_op))])
            id = next(iter_op)
            pos = np.dot(np.linalg.inv(proj_mat), persPos[i,:].reshape(3,1)).squeeze()
            pos = np.dot(200/pos[2], pos) # 200 in the numerator is the 100*2 which is conversion of meters to cm (1m = 100cm) and cm to pixels (1cm = 2px)
            tracker[i, :2] = np.array([int((pos[0])), int((pos[1]))])
            tracker[i, 2] = id
            tracker[i, 3] = device_id[i]
            tracker[i, 4:] = features[i]


        return tracker


    except Exception as e:
        return e
    
def load_mat(path):
    '''
    path: This is the path of the folder containing two subfolders namely camMat and projMat

    This function helps in loading the matrices from .npy file
    '''

    cam_folder = os.path.join(path, r"camMat")
    cam_path = os.listdir(cam_folder)
    cam_path = list(map(lambda x: os.path.join(cam_folder, x), cam_path))

    proj_folder = os.path.join(path, r"projMat")
    proj_path = os.listdir(proj_folder)
    proj_path = list(map(lambda x: os.path.join(proj_folder, x), proj_path))

    proj_mat = []
    vecPx = []

    for path in cam_path:
         cam_pos = np.load(path).ravel()
         vecPx.append((cam_pos*100*2).astype('int16'))

    for path in proj_path:
         p = np.load(path).astype(np.float32)
         p = np.delete(p, 2, 1)
         proj_mat.append(p)

    return proj_mat, vecPx  


