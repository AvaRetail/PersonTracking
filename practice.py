# import numpy as np
# op = [1443.0, 1864.0, 939.0, 1403.0, 1313.0, 1337.5]
# P = np.load("projection.npy").astype(np.float32)
# p = np.delete(P, 3, 0)
# p = np.delete(p, 2, 1)
# print(p)

# try: 
#     # op = list(map(eval, op))
#     iter_op = iter(op)
#     persPos = np.ones((int(len(op)/2),3), np.int16)
#     for i in range(persPos.shape[0]):
#         persPos[i,:2] = np.array([int(next(iter_op)), int(next(iter_op))])
#         pos = np.matmul(np.linalg.inv(p), persPos[i,:].reshape(3,1))
#         print(pos) 

# except Exception as e:
#     print(e)

# import cv2
# camMap = cv2.imread("floorMap.png")
# pos = [499, 432, 200]

# cv2.imshow("img", cv2.circle(camMap.copy(), (int(pos[0]), int(pos[1])), 10, (0, 255, 0), 2))
# cv2.waitKey(0)

# import numpy as np

# cam_mat = np.array([[1.82625961e+03, 0.00000000e+00, 1.25134147e+03],
# [0.00000000e+00, 1.54135456e+03, 7.05457440e+02],
# [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

# def make_callback(result):
#     def callback(data):
#         result.append(data)
#     return callback

# # Create a closure to store the result
# result = []
# callback = make_callback(result)

# # Call the callback and store the result in the closure
# callback("Hello World")

# # Print the result
# print(result)

# import threading

# # Create a lock to synchronize access to the data
# lock = threading.Lock()

# # Create a list to store the data
# data = []

# def on_message_system_1(client, userdata, msg):
#     with lock:
#         data.append(msg.payload)
#         # Check if both responses have arrived
#         if len(data) == 2:
#             # Apply the operation on the data
#             result = operation(data[0], data[1])
#             print(result)

# def on_message_system_2(client, userdata, msg):
#     with lock:
#         data.append(msg.payload)
#         # Check if both responses have arrived
#         if len(data) == 2:
#             # Apply the operation on the data
#             result = operation(data[0], data[1])
#             print(result)

# # Connect to the MQTT broker and subscribe to the topics
# client = mqtt.Client()
# client.on_message = on_message_system_1
# client.subscribe("system1")

# client.on_message = on_message_system_2
# client.subscribe("system2")

# client.connect("localhost")
# client.loop_start()

# for i in []:
#     print(i)

# import numpy as np
# data = [np.array([1]), np.array([1])]

# print(data[0]!=None and data[1]!=None)

# import cv2
# from utils.operations import capture

# # read image
# img = capture("rtsp://admin:_056pwjr@192.168.21.201")
# print(img.shape)

# # show image
# cv2.imshow('image', cv2.resize(img,(0,0),fx=0.5, fy=0.5))

# # define the events for the
# # mouse_click.
# def mouse_click(event, x, y,
# 				flags, param):
	

# 	if event == cv2.EVENT_LBUTTONDOWN:
# 		print(x, y)

		


# cv2.setMouseCallback('image', mouse_click)

# cv2.waitKey(0)

# # close all the opened windows.
# cv2.destroyAllWindows()



# if not(self.updated) and self.state=='t':
#     self.state = 'c'
    
# elif not(self.updated) and self.state=='c':
#     self.x = pers[0]
#     self.y = pers[1]
#     self.updated = True
#     self.time_since_updated = 0

# from utils.operations import *
# img = capture("rtsp://admin:_056pwjr@192.168.21.201")
# imShow(img, 1)


# Python program to explain
# cv2.polylines() method

# import cv2
# import numpy as np


# image = np.full((500, 500, 3), 255,  dtype=np.uint8)


# # Window name in which image is
# # displayed
# window_name = 'Image'

# # Polygon corner points coordinates
# pts = np.array([[25, 70], [25, 160],
# 				[110, 200], [200, 160],
# 				[200, 70], [110, 20]],
# 			np.int32)

# pts = pts.reshape((-1, 1, 2))

# isClosed = True

# # Blue color in BGR
# color = (255, 0, 0)
# # Line thickness of 2 px
# thickness = 2

# image = cv2.polylines(image, [pts],
# 					isClosed, color, thickness)
# image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# ret, threshold = cv2.threshold(image, 0, 1, cv2.THRESH_BINARY)


# contours, hierarchy = cv2.findContours(image=threshold, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

# cv2.imshow("img", image)
# cv2.waitKey(0)
		
# cv2.destroyAllWindows()
# a = [5,6,7,8]
# b = []
# for i in a:
#     for i in a:
#         b.append(a*a)
# import numpy as np
# x = np.array([    0.71094,           0,      2.7803,           0,           0,           0,           0,           0,     0.41895,           0,       1.734,           0,       1.618,      
#      0,      1.3147,      2.3622,     0.44143,           0,           0,     0.69746,      2.0868,           0,           0,  0.00013204,
#         1.3351e-06,      1.7757,           0,     0.38769,      0.1188,     0.07128,  8.7695e-06,           0,           0,           0,       2.183,           0,           0,  4.3348e-05,       
#     0,           0,      2.8209,     0.42446,           0,           0,     0.38333,      4.5497,           0,      1.1494,
#                  0,           0,           0,           0,           0,     0.60785,      2.9256,           0,     0.99136,      4.3097,           0,           0,           0,           0,      1.0757,           0,           0,           0,      1.0591,      3.1397,     0.93147,  4.0065e-07,           0,           0,
#                  0,           0,           0,     0.59102,           0,      0.8599,     0.25134,      0.8052,           0,           0,           0,     0.30076,      2.7084,  8.9394e-06,       
#     0,           0,      1.7191,           0,           0,           0,       1.528,           0,      1.7019,           0,
#              1.216,           0,           0,     0.03501,           0,           0,           0,           0,     0.25124,  4.6749e-08,           0,           0,      2.7522,           0,       
#     0,     0.13412,      1.7097,           0,   0.0076949,           0,  1.9294e-07,      2.1061,      1.0549,           0,
#             2.3648,           0,           0,           0,      1.0889,  1.6183e-06,      1.0123,      1.2839,      1.5033,           0,      3.9153,           0,     0.86628,      2.9259,       
#     0,   4.964e-08,           0,           0,           0,           0,     0.67504,           0,     0.68487,           0,
#             3.8422,      2.3379,           0,           0,           0,           0,           0,      3.2318,    0.053109,           0,           0,           0,       1.586,   0.0019534,     0.42824,     0.11453,           0,           0,           0,           0,      4.9687,           0,           0,      0.4114,
#             4.2118,  0.00067667,     0.10514,           0,           0,     0.99258,      1.0633,           0,  3.2458e-06,           0,      1.3814,       0.761,     0.97572,           0,       
#     0,           0,     0.33587,           0,           0,      2.2182,           0,           0,      3.1222,           0,
#            0.73092,      1.9088,       5.888,           0,      1.1511,      3.9732,           0,           0,           0,           0,      3.6272,           0,           0,           0,       
#     0,           0,      1.3854,     0.27253,      5.8971,           0,           0,      16.594,      1.7458,  0.00011843,
#            0.12357,           0,           0,           0,      1.9376,     0.37785,           0,  7.3836e-08,      1.1986,           0,           0,       3.518,           0,           0,      0.8894,      1.4113,           0,       1.248,      2.5503,           0,           0,           0,     0.27098,           0,
#                  0,      4.0244,     0.53755,      1.5443,    0.023407,           0,           0,           0,  4.2096e-05,      4.3969,      3.3378,      1.1105,     0.97662,  6.2285e-09,       
#     0,           0,           0,           0,           0,      2.7859,           0,           0,     0.32134,      2.2055,
#             3.3659,     0.48487,      2.2613,     0.93652,           0,      2.4039,       2.406,     0.57045,      3.0732,     0.73363,           0,      1.3453,      2.0796,           0,       
#     0,           0,           0,           0,      0.1614,           0,       3.866,           0,           0,           0,
#           0.027871,      1.8154,    0.016568,      2.3605,       2.291,           0,           0,           0,           0,           0,           0,           0,           0,           0,       
# 1.793,           0,      2.7971,       1.727,      3.1465,  2.6976e-06,           0,           0,           0,     0.45967,
#                  0,           0,      0.4809,           0,           0,           0,     0.51083,           0,           0,           0,           0,   1.106e-05,      2.2118,           0,      1.5378,           0,  2.1451e-06,      1.5616,       1.599,           0,           0,      1.2988,           0,           0,
#                  0,           0,           0,    0.052003,      2.3157,      1.7092,           0,           0,     0.72814,           0,           0,     0.49756,           0,           0,       
#     0,     0.18156,           0,           0,           0,      1.2955,      1.0002,           0,           0,           0,
#            0.24211,  0.00016616,           0,    0.064741,           0,     0.11011,       1.026,           0,           0,           0,           0,           0,     0.93026,      1.7548,  7.2136e-06,           0,      2.4233,      2.6237,       1.112,           0,           0,     0.39338,     0.28124,      3.1073,
#                  0,      4.0671,      3.3132,    0.003698,           0,      1.3141,           0,   0.0068488,           0,  1.0131e-05,      1.7591,      2.4547,           0,      2.3257,      1.1966,      1.7859,      1.0156,           0,  0.00030668,           0,      3.8065,           0,           0,           0,
#            0.89765,     0.34219,      5.8488,      0.8557,      1.4232,           0,           0,           0,     0.96415,           0,           0,           0,           0,           0,       
#     0,           0,           0,           0,           0,  4.3411e-05,           0,           0,      1.8677,      1.7711,
#              1.257,           0,           0,       5.195,      1.5585,     0.34151,           0,           0,           0,      4.6157,           0,           0,     0.35662,           0,   0.0067119,           0,           0,      4.9624,           0,      0.5553,           0,      0.6514,           0,           0,
#                  0,           0,      3.8611,           0,           0,     0.42886,     0.47353,           0,           0,   0.0027841,      2.2987,           0,           0,     0.38305,       
#     0,  2.8985e-07,    0.056896,           0,           0,      1.3557,      2.2175,     0.22626,           0,      1.7536,
#             1.2949,      1.2324,    0.095301,     0.60617,     0.33297,     0.92564,           0,           0,           0,           0,      3.8604,           0,     0.12684,           0,       
#     0,      1.6129,           0,           0,           0,           0,           0,           0,           0,     0.71043,
#                  0,           0,      0.6386,           0,           0,      2.4864,           0,           0])

# # print(str(x[:]).replace('[','').replace(']', ''))
# import sys
# print(sys.getsizeof(eval(str(2.8985e-07))))
# print(x[0].nbytes)
# print(x.dtype)

import numpy as np

# np.random.seed(32)
# x = np.random.randn(100,5)

# print(x[1].shape)

lst = [5, 10, [11,15]]

str_list = str(lst)

print(str_list.replace('[', '').replace(']',''))



