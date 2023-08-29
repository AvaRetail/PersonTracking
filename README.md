# smoothShop

## Motivation
A solution like smooth shop involves many things that run in the background like object tracking, sensor fusion, virtual floor maps, pose estimation and many more. This repository cotains the code related to subset of the smooth shop in python; the idea is that we need to keep track of the customer entered into the store in a virtual space. why do we need to have a virtual space in the first place, this is because the virtual space helps us in creating the zones, product location and also sensor location. So, when a customer is tracked in the virtual space picks up a product which is also connected the same virtual space helps us in tracking the products along with the customer by some triggering events.

## Architecture
- The code related to tracking algorithm has been cloned.
- Each camera is assosciated with a seperate GPU. i.e., frames coming from camera-A is sent only to the GPU-1.
- POSENET is used for the pose estimation.
- The track ids which are independent from each system will be sent to a single system along with the foot position of 2D pose estimation using MQTT broker.
- all of these independent results has to be merged together to make a single id for a customer.

## Pre-Requisites
- There is one more important task that needs to be done is the Intrinsic and Extrinsic calibration for both the IP Cameras.
- This helps us in mapping the points from 2D Image space to the world co-ordinates.
