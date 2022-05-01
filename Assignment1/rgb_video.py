#!/usr/bin/env python3

import cv2
import depthai as dai
import time
from depthai_sdk.fps import FPSHandler
# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutVideo = pipeline.create(dai.node.XLinkOut)

xoutVideo.setStreamName("video")

# Properties
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setVideoSize(1280,720)

xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)

# Linking
camRgb.video.link(xoutVideo.input)
# Connect to device and start pipeline
start_time = time.time()
x = 1
counter = 0
count=0
with dai.Device(pipeline) as device:

    video = device.getOutputQueue(name="video", maxSize=1, blocking=False)

    while True:
        videoIn = video.get()
        Frame=videoIn.getCvFrame()
        counter+=1
        font = cv2.FONT_HERSHEY_SIMPLEX
        if (time.time() - start_time) >= 1 :
                fps=counter
                counter = 0
                start_time = time.time()
        cv2.putText(Frame, str(fps)+' '+str(camRgb.getVideoSize()), (7, 70), font, 1, (100, 255, 0), 1, cv2.LINE_AA)
        cv2.imshow("video", Frame)
        if cv2.waitKey(1)==ord('p'):
            count+=1
            cv2.imwrite('image'+str(count)+'.jpg',Frame)
        if cv2.waitKey(1) == ord('q'):
            break
