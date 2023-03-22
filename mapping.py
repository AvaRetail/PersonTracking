import cv2
import numpy as np
import paho.mqtt.client as paho
import paho.mqtt as mqtt 

from correct import undistort
from utils.operations import capture, imShow

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):

    global camMap
    global proj_mat
    global tracker

    op = msg.payload.decode().replace(' ','').replace('[','').replace(']','').rsplit(",")
    # print(op)
    camMapClone = camMap.copy() # Copy helped me in removing the cirlce on image after each iteration

    try: 
        op = list(map(eval, op)) # converts the string into list of floating numbers
        iter_op = iter(op) #converts the list into iterable object
        persPos = np.ones((int(len(op)/3),3), np.int16) #creating a numpy array to store the person positions
        nPers = persPos.shape[0]
        for i in range(nPers):
            persPos[i,:2] = np.array([int(next(iter_op)), int(next(iter_op))])
            pos = np.dot(np.linalg.inv(proj_mat), persPos[i,:].reshape(3,1)).squeeze()
            pos = np.dot(200/pos[2], pos) # 200 in the numerator is the 100*2 which is conversion of meters to cm (1m = 100cm) and cm to pixels (1cm = 2px)
            cv2.circle(camMapClone, (int(pos[0]), int(pos[1])), 10, (0, 255, 0), 2)
            cv2.putText(camMapClone, f'id_{next(iter_op)}', (int(pos[0]), int(pos[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            # cv2.waitKey(10)

    except Exception as e:
        print(e)

    # cv2.imshow("img", camMapClone)
    result.write(camMapClone)
    # cv2.waitKey(1000)


class PahoMqtt():
    def __init__(self) -> None:
        self.client = paho.Client(client_id="reciever", userdata=None, protocol=paho.MQTTv5)
        self.client.on_connect = on_connect

        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set("bumpeet", "Chetan@123")
        self.client.connect("0f1ffe2b526445fcb8f7309446340bd9.s2.eu.hivemq.cloud", 8883)

        self.client.on_subscribe = on_subscribe
        self.client.on_message = on_message

        self.client.subscribe("strongSort/ati-g2", qos=0)


def main():

    global camMap
    global proj_mat
    global result
    global tracker

    flrmap = cv2.imread(r"images\\floorMap.png")

    P = np.load("files\projMat\projMat_208.npy").astype(np.float32)
    proj_mat = np.delete(P, 2, 1)

    # intMat201 = np.load("files\int_cam_mat_208.npy")
    # distMat201 = np.load("files\dist_coeff_208.npy")

    # undist = undistort(intMat201, distMat201)

    camPos = np.load("files\camMat\camPos_208.npy").ravel()

    vecPx = (camPos*100*2).astype('int16')

    camMap = cv2.rectangle(flrmap.copy(), (vecPx[0]-20,vecPx[1]-20), (vecPx[0]+20, vecPx[1]+20), (255,0,0))

    result = cv2.VideoWriter('filename.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, (flrmap.shape[1], flrmap.shape[0]))

    clnt = PahoMqtt()
    clnt.client.loop_forever()


if __name__=="__main__":
    main()


