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
from pytz import timezone

from socket import *

import argparse

import math

import tempfile
import requests

warnings.filterwarnings('ignore')



def main(yolo):

    # Definition of the parameters
    max_cosine_distance = 0.3
    nn_budget = None
    nms_max_overlap = 1.0

    width=1280
    height=720
    rfps=10
    
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
    cam_ip = full_cam_addr.replace(args.cam_cmd, "").replace("rtsp://camera:Camera123@", "")
    print(full_cam_addr)
    print(key)

  
    if asyncVideo_flag :
        print("load videofile")
        video_capture = VideoCaptureAsync(args.videofile)
    elif ipcamera_flag :
        print("load ipcamera")
        video_capture = cv2.VideoCapture(full_cam_addr)
        #video_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        rfps = video_capture.get(cv2.CAP_PROP_FPS)
        print("fps:{}width:{}height:{}".format(rfps, width, height))
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
    
    i = 0

    savetime = 0
    if not args.maskoff:
        maskbgi = Image.new('RGB',(int(width), int(height)) , (0,0,0))
        mask = Image.open(args.maskdir + 'mask' + args.ipaddress[-1] + '.png').convert("L").resize(size=(int(width), int(height)), resample=Image.NEAREST)

    while True:
        nowtime = datetime.datetime.now(timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S.%f')
        if not args.jpegmode:
            ret, frame = video_capture.read()  # frame shape 640*480*3
            
            if not ret:
                print('cant read')
                video_capture = cv2.VideoCapture(full_cam_addr)
                continue
            t1 = time.time()            
            try:
                image = Image.fromarray(frame[...,::-1])  # bgr to rgb
            except TypeError:
                video_capture = cv2.VideoCapture(full_cam_addr)
                continue
        else:
            res = requests.get('http://192.168.25.61/SnapshotJPEG')
            image = None
            with tempfile.NamedTemporaryFile(dir='./') as fp:
                fp.write(res.content)
                fp.file.seek(0)
                frame = cv2.imread(fp.name)
                image = Image.fromarray(frame[...,::-1])

        image = Image.composite(maskbgi, image, mask)
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
            sd.send_amqp(sd.create_jsondata(cam_ip, nowtime, time.time() - t1, car_data, args.jsonfile, args.json_path, i), key, args.AMQPHost)
            i += 1

        if not asyncVideo_flag:
            fps = (fps + (1./(time.time()-t1))) / 2
            print("FPS = %f"%(fps))
        
        
        ### 読み飛ばし処理を追加 ###
        if not args.jsonfile and args.skip:
            if fps <=10:
                for _i in range (int(math.ceil(rfps/fps)) - 1) :
                    ret, frame = video_capture.read()
            

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
    parser.add_argument("-maskoff", action="store_true")
    parser.add_argument("-jpegmode", action = 'store_true')

    parser.add_argument("--ipaddress", default='192.168.25.51', type=str)
    parser.add_argument("--AMQPHost", default = 'localhost', type=str)
    parser.add_argument("--key", default = 'jp.chiba.kashiwa.kashiwanoha.25.sensor.', type=str)
    
    parser.add_argument("--cam_ip", default="rtsp://camera:Camera123@192.168.25.6", type=str)
    parser.add_argument("--cam_cmd", default="/mediainput/h265?tcp", type=str)
    parser.add_argument("--videofile", default="/home/aj1m0n/MOT/data/C0133-480p.mp4", type=str)
    parser.add_argument("--json_path", default='/home/aj1m0n/MOT/data/json/', type=str)
    parser.add_argument("--maskdir", default='../../mask/', type=str)
    args = parser.parse_args()
    main(YOLO())
