import cv2
import numpy as np
import paho.mqtt.client as paho
import paho.mqtt as mqtt 
import time
import sys

from merging import initiateBlob, continueBlob, doneBlob
from utils.easy import *

def on_message(client, userdata, msg):
    global flrmap
    global shoppers
    global filtr
    global data

    no_of_cams = 2

    if msg.topic == "strongSort/201" and len(data) == 0: #and len(data) == 0
            trackerA = operation(msg, proj_mat_201)
            data.append(trackerA)
            # data.append()
            # print("data1:     ", trackerA)

    if msg.topic == "strongSort/208" and len(data) == 1: #and len(data) == 1
            trackerB = operation(msg, proj_mat_208)
            data.append(trackerB)
            # print("data2:     ", trackerB)

    if len(data)==no_of_cams:
        # print(f'The data is {data}')
        camMapClone = flrmap.copy()

        if filtr and instanceCheck(data):
            # shoppers = initiateBlob(data)
            # shoppers = doneBlob(shoppers)
            # filtr = False

            shoppers = initiateBlob(data)
            shoppers = doneBlob(shoppers)
            filtr = False

        elif not(filtr) and instanceCheck(data):
            for val in data:
                if isinstance(val, np.ndarray):
                    shoppers = continueBlob(val, shoppers)
            shoppers = doneBlob(shoppers)
        
        camMapClone = drawShoppers(camMapClone, shoppers)
        # cv2.imshow("SmoothShop", camMapClone)
        # cv2.waitKey(50)
        result.write(camMapClone)
        data.clear()

class PahoMqtt():
    def __init__(self, client_name) -> None:
        self.client = paho.Client(client_id = client_name, userdata=None, protocol=paho.MQTTv5)
        self.client.on_connect = on_connect

        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set("bumpeet", "Chetan@123")
        self.client.connect("0f1ffe2b526445fcb8f7309446340bd9.s2.eu.hivemq.cloud", 8883)

        self.client.on_subscribe = on_subscribe

        sub_list = [("strongSort/201", 0), ("strongSort/208", 0)]

        self.client.on_message = on_message
        self.client.subscribe(sub_list)

def check(data):
    global flrmap
    global filtr
    global shoppers

    if len(data)==2:
        print(f'The data is {data}')
        camMapClone = flrmap.copy()

        if filtr and instanceCheck(data):
            shoppers = initiateBlob(data)
            shoppers = doneBlob(shoppers)
            filtr = False

        elif not(filtr) and isinstance(data[0], np.ndarray) and isinstance(data[1], np.ndarray):
            for i in data:
                shoppers = continueBlob(i, shoppers)
            shoppers = doneBlob(shoppers)
        
        camMapClone = drawShoppers(camMapClone, shoppers)
        cv2.imshow("SmoothShop", camMapClone)
        cv2.waitKey(50)

def main(filePath: str):
    global flrmap
    global proj_mat_201
    global proj_mat_208

    proj_mat, cam_pos = load_mat(filePath)
    proj_mat_201, proj_mat_208 = proj_mat[0], proj_mat[1]

    for i, vecPx in enumerate(cam_pos):
        cv2.rectangle(flrmap, (vecPx[0]-20, vecPx[1]-20), (vecPx[0]+20, vecPx[1]+20), (255, 0, 0))
        cv2.putText(flrmap, f'cam_{i+1}', (vecPx[0], vecPx[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)

    clnt = PahoMqtt("reciever")
    clnt.client.loop_forever()

def verify(filePath: str):
    global flrmap
    global proj_mat_201
    global proj_mat_208
    global filtr
    global shoppers

    proj_mat, cam_pos = load_mat(filePath)
    proj_mat_201, proj_mat_208 = proj_mat[0], proj_mat[1]

    for vecPx in cam_pos:
        cv2.rectangle(flrmap, (vecPx[0]-20,vecPx[1]-20), (vecPx[0]+20, vecPx[1]+20), (255, 0, 0))

    n = 100

    np.random.seed(32)
    data = np.random.randint(60, 400, (n, 2, 2, 4))
    # ids = np.random.randint(0, 10, (n, 2))
    ids1 = np.zeros((100,))
    ids2 = np.ones((100,))
    ids3 = np.full((100,), 10)
    ids4 = np.full((100,), 20)

    # data[:, 0, :, 2], data[:, 1, :, 2] = np.resize(ids[:, 0], (n, 1)) , np.resize(ids[:, 1], (n, 1)) 
    data[:, 0, 0, 2], data[:, 0, 1, 2] = ids1, ids2
    data[:, 1, 0, 2], data[:, 1, 1, 2] = ids3, ids4

    data[:, 0, :, 3] = np.full((100,2), 201 )
    data[:, 1, :, 3] = np.full((100,2), 208 )
    

    for i, val in enumerate(data):
         check([val[0], val[1]])
         time.sleep(0.05)

if __name__=="__main__":

    # sys.stdout = open(r"D:\Chetan\Documents\python_scripts\smoothShop\goat.txt", "w")
    global flrmap
    global proj_mat_201
    global proj_mat_208
    global filtr
    global shoppers
    global data
    global write

    filtr = True
    shoppers = []
    data = []

    flrmap = cv2.imread(r"images\\floorMap.png")
    filePath = r"D:\Chetan\Documents\python_scripts\smoothShop\files"

    result = cv2.VideoWriter('filename.avi', 
                        cv2.VideoWriter_fourcc(*'MJPG'),
                        5, (flrmap.shape[1], flrmap.shape[0]))

    main(filePath)
    # verify(filePath)
    cv2.destroyAllWindows()
