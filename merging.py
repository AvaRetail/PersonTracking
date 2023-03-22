import numpy as np
import math
from utils.operations import *
import sys

class shopper():
    count = 100

    def __init__(self, pers) -> None:
        self.x = pers[0]
        self.y = pers[1]
        self.id = self.count
        self.storage = [pers[2]]
        self.device = [pers[3]]
        self.updated = True
        self.time_since_updated = 0
        self.state = 't'
        self.feature = pers[4:]


    def update(self, pers):
        if not(self.updated):
            self.x = pers[0]
            self.y = pers[1]
            self.feature = pers[4:]
            self.updated = True
            self.time_since_updated = 0

def cosine(a,b):
    x =np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    print('The cosine value for your reference: ', x)
    return x

def subInitiate(b, shops):
    threshold = 0.5
    idx = []

    for i, val in enumerate(b):
        for org in shops:
                
            if cosine(org.feature, val[4:]) >= threshold:
                org.storage.append(val[2])
                org.device.append(val[3])
                idx.append(i)
                break

    for i, val in enumerate(b):
        if not(i in idx):
            shops.append(shopper(val))
            shopper.count += 1

    return shops

def initiateBlob(data):
    shops = []
    
    for i, val in enumerate(data):
        if i==0:
            try:
                for track in val:
                    shops.append(shopper(track)) # this will trrigger only if data is [cam_1 data, None] or [cam_1 data, cam_2 data]
                    shopper.count += 1
            except:
                continue # This will be triggered if data is [None, cam_2 data]

        else:
            try:
                shops = subInitiate(val, shops)

            except:
                continue

    return shops

def continueBlob(tracker, shops: list[shopper]) -> list[shopper]:
    threshold = 0.5
    idx = []
    ids = []

    for i, val in enumerate(tracker):
        for org in shops:
            if (val[2] in org.storage):
                if org.device[org.storage.index(val[2])] == val[3]: # Here I'm checking the corresponding device id of org.storage with the val[3]
                    org.update(val)
                    idx.append(i)
                   
                    break

                elif cosine(org.feature, val[4:]) >= threshold:
                    org.update(val) 
                    # org.storage.append(val[2])
                    # org.device.append(val[3])
                    idx.append(i)
                    break    
                    


            elif cosine(org.feature, val[4:]) >= threshold:
                org.update(val) # This step is included becuase if thre's an id switch we can update but I don't think this is a good idea
                org.storage.append(val[2])
                org.device.append(val[3])
                idx.append(i)
                break                    


                    

    for i, val in enumerate(tracker):
        if not(i in idx):
            shops.append(shopper(val))
            shopper.count += 1

    return shops

def doneBlob(shops):
    # distance=[]
    # for shop1 in shops:
    #     for shop2 in shops:
    #         distance.append(measure([shop1.x, shop1.y], [shop2.x, shop2.y]))


        
    for i, shop in enumerate(shops):
        rem_shop_list=[]
        if shop.time_since_updated > 60:
            rem_shop_list.append(shop)
        
        shop.updated  = False
        shop.time_since_updated += 1

    map(lambda x: shops.remove(x), rem_shop_list) # removing the shoppers from the shops list based on the if condition shown above

    return shops

def measure(x1, x2):
    return math.sqrt( (x2[0]-x1[0])**2 + (x2[1]-x1[1])**2 )



if __name__=="__main__":
    dt = Profile()
    data = np.array([[[[225, 434, 19]], [[230, 441, 3]]],
                     [[[225, 434, 19]], [[230, 441, 3]]],
                     [[[220, 430, 20]], [[241, 450, 4]]],
                     [[[251, 478, 20]], [[280, 480, 4]]],
                     [[[300, 510, 21]], [[270, 470, 4]]]])
    filtr = True
    cam = data.shape[1]
    shops = None
    for i, val in enumerate(data):
        if filtr:
            shops = initiateBlob(val[0], val[1])
            filtr = False
        else:
            for i in range(cam):
                with dt:
                    shops = continueBlob(val[i], shops)
                    shops = doneBlob(shops)
        
        for shop in shops:
            print(f"The position of shopper-{shop.id} X is {shop.x}, Y is {shop.y}")
