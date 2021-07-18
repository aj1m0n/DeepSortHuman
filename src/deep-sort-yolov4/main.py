#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

from timeit import time
import warnings
import cv2
import numpy as np
from PIL import Image
from yolo import YOLO

from deep_sort import preprocessing
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.detection_yolo import Detection_YOLO
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
from tools import send_data as sd
import imutils.video
from videocaptureasync import VideoCaptureAsync

import datetime

from socket import *

import argparse

import math

warnings.filterwarnings('ignore')



def main(yolo):

    # Definition of the parameters
    max_cosine_distance = 0.3
    nn_budget = None
    nms_max_overlap = 1.0
    
    # Deep SORT
    model_filename = 'model_data/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename, batch_size=1)
    
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    tracker = Tracker(metric)

    tracking = args.tracking
    writeVideo_flag = args.writeVideo_flag
    asyncVideo_flag = args.asyncVideo_flag
    webcamera_flag = args.webcamera_flag
    ipcamera_flag = args.ipcamera_flag
    udp_flag = args.udp_flag

    full_cam_addr, key = sd.set_address(args.ipaddress, args.cam_ip, args.cam_cmd, args.key)
    cam_ip = full_cam_addr.replace(args.cam_cmd, "")
    print(full_cam_addr)
    print(key)

  
    if asyncVideo_flag :
        print("load videofile")
        video_capture = VideoCaptureAsync(args.videofile)
    elif ipcamera_flag :
        print("load ipcamera")
        video_capture = cv2.VideoCapture(args.cam_ip)
        # video_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        print("fps:{}width:{}height:{}".format(fps, width, height))
    elif webcamera_flag :
        print("load webcamera")
        video_capture = cv2.VideoCapture(0)
    else:
        print("load videofile")
        video_capture = cv2.VideoCapture(args.videofile)
        
    # video_capture.start()

    if writeVideo_flag:
        if asyncVideo_flag:
            w = int(video_capture.cap.get(3))
            h = int(video_capture.cap.get(4))
        else:
            w = int(video_capture.get(3))
            h = int(video_capture.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output_yolov4.avi', fourcc, 30, (w, h))
        frame_index = -1

    if udp_flag:
        HOST = ''
        PORT = 5000
        address = '192.168.2.255'
        sock =socket(AF_INET, SOCK_DGRAM)
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        sock.bind((HOST, PORT))
        
    fps = 0.0
    fps_imutils = imutils.video.FPS().start()
    
    i = 0

    savetime = 0
    
    while True:
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        ret, frame = video_capture.read()  # frame shape 640*480*3
        t1 = time.time()
          
        # if time.time() - savetime >= 30: 
        #     print('save data') 
        #     cv2.imwrite("/workspace/images/image.png", frame)
        #     savetime = time.time()
        image = Image.fromarray(frame[...,::-1])  # bgr to rgb
        boxes, confidence, classes = yolo.detect_image(image)

        if tracking:
            features = encoder(frame, boxes)

            detections = [Detection(bbox, confidence, cls, feature) for bbox, confidence, cls, feature in
                        zip(boxes, confidence, classes, features)]
        else:
            detections = [Detection_YOLO(bbox, confidence, cls) for bbox, confidence, cls in
                        zip(boxes, confidence, classes)]

        # Run non-maxima suppression.
        boxes = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        indices = preprocessing.non_max_suppression(boxes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]
        car_data = {}
        if tracking:
            # Call the tracker
            tracker.predict()
            tracker.update(detections)

            for track in tracker.tracks:
                if not track.is_confirmed() or track.time_since_update > 1:
                    continue
                bbox = track.to_tlbr()
                car_data[str(track.track_id)] = [int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])]
                if udp_flag:
                    sock.sendto(message.encode('utf-8'), (address, PORT))
            if car_data:
                sd.send_amqp(sd.create_jsondata(cam_ip, nowtime, time.time() - t1, car_data, args.jsonfile, args.json_path, i), key, args.AMQPHost)
                i += 1


        for det in detections:
            bbox = det.to_tlbr()
            score = "%.2f" % round(det.confidence * 100, 2) + "%"
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 0, 0), 2)
            if len(classes) > 0:
                cls = det.cls
                cv2.putText(frame, str(cls) + " " + score, (int(bbox[0]), int(bbox[3])), 0,
                            1.5e-3 * frame.shape[0], (0, 255, 0), 1)

        #cv2.imshow('', frame)

        if writeVideo_flag: # and not asyncVideo_flag:
            # save a frame
            out.write(frame)
            frame_index = frame_index + 1

        fps_imutils.update()

        if not asyncVideo_flag:
            fps = (fps + (1./(time.time()-t1))) / 2
            print("FPS = %f"%(fps))
        
        # Press Q to stop!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        ### 読み飛ばし処理を追加 ###
        if not args.jsonfile and args.skip:
            if fps <=10:
                for _i in range (int(math.ceil(10/fps)) - 1) :
                    ret, frame = video_capture.read()
            

    fps_imutils.stop()
    print('imutils FPS: {}'.format(fps_imutils.fps()))

    if asyncVideo_flag:
        video_capture.stop()
    else:
        video_capture.release()

    if writeVideo_flag:
        out.release()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    print('ver1.2')
    parser = argparse.ArgumentParser()
    parser.add_argument("-tracking", action = 'store_false')
    parser.add_argument("-writeVideo_flag", action = 'store_true')
    parser.add_argument("-asyncVideo_flag", action = 'store_true')
    parser.add_argument("-webcamera_flag", action = 'store_true')
    parser.add_argument("-ipcamera_flag", action = 'store_true')
    parser.add_argument("-jsonfile", action = 'store_true')
    parser.add_argument("-udp_flag", action = 'store_true')
    parser.add_argument("-skip", action = 'store_false')

    parser.add_argument("--ipaddress", default='192.168.25.51', type=str)
    parser.add_argument("--AMQPHost", default = 'localhost', type=str)
    parser.add_argument("--key", default = 'jp.chiba.kashiwa.kashiwanoha.25.sensor.', type=str)
    
    parser.add_argument("--cam_ip", default="rtsp://camera:Camera123@192.168.10.6", type=str)
    parser.add_argument("--cam_cmd", default="/mediainput/h264", type=str)
    parser.add_argument("--videofile", default="/home/aj1m0n/MOT/data/C0133-480p.mp4", type=str)
    parser.add_argument("--json_path", default='/home/aj1m0n/MOT/data/json/', type=str)
    args = parser.parse_args()
    main(YOLO())
