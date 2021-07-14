# Introduction
This project was inspired by:
* https://github.com/nwojke/deep_sort
* https://github.com/Ma-Dan/keras-yolo4
* https://github.com/Qidian213/deep_sort_yolov3
* https://github.com/LeonLok/Deep-SORT-YOLOv4

## Performance
Real-time FPS with video writing:
* ~10.6fps with YOLO v4

Turning off tracking gave ~12.5fps with YOLO v4.

All tests were done using an Nvidia Jetson Xavier NX.

However,using webcamera is much slower than loading video.(~2.0fps)

# Docker image

```
docker pull aj1m0n/deep_sort:latest
```

# Quick start
## Settings
### Directory structure

```
/
├ home/
│  └ username/
│       └ workspace/
│           ├ Deep_Sort/
│           │    └ src/
│           │        └ deep-sort-yolov4/
│           │            └ main.py
│           │            └ model_data/
│           │                └ yolov4.weights
│           └ data/
│               └ C0133_v4.mp4
```
[Download Yolov4](https://drive.google.com/open?id=1cewMfusmPjYWbrnuJRuKhPMwRe_b9PaT) to model_data

[Download video](
https://drive.google.com/file/d/1Gri4rt8zx7BLPza_-E8FEsMqnMyB93A4/view?usp=sharing) to ~/workspace/data/


### Pull Docker image to Jetson Xavier NX
```
docker pull aj1m0n/deep_sort:latest
```

Run docker without sudo
```
# dockerグループがなければ作る
sudo groupadd docker

# 現行ユーザをdockerグループに所属させる
sudo gpasswd -a $USER docker

# dockerデーモンを再起動する (CentOS7の場合)
sudo systemctl restart docker

# exitして再ログインすると反映される。
exit
```

### Run docker
make workspce directory.
```
mkdir ~/workspace/
```
run docker image with webcamera(/dev/video0).
If you do not want to use webcamera, delete --device /dev/video0:/dev/video0.
```
docker run -it -v ~/workspace/:/workspace/ --device /dev/video0:/dev/video0 --runtime nvidia --network host aj1m0n/deep_sort:latest
```

### Convert keras format
convert the Darknet YOLO v4 model  to a Keras model by modifying `convert.py` accordingly and run:
```
python3 convert.py
```

### Run script
```
python3 main.py
```
### Normal Deep SORT
By default, tracking and video writing is on and asynchronous processing is off.
Parser example:
```
parser.add_argument("-tracking", action = 'store_false')
parser.add_argument("-writeVideo_flag", action = 'store_true')
parser.add_argument("-asyncVideo_flag", action = 'store_true')
parser.add_argument("-webcamera_flag", action = 'store_true')
parser.add_argument("-ipcamera_flag", action = 'store_true')
parser.add_argument("-jsonfile", action = 'store_true')
parser.add_argument("-udp_flag", action = 'store_true')
parser.add_argument("-skip", action = 'store_false')
parser.add_argument("--AMQPHost", default = 'localhost', type=str)
parser.add_argument("--key", default = 'jp.chiba.kashiwa.kashiwanoha.25.sensor.1', type=str)

parser.add_argument("--cam_ip", default="rtsp://camera:Camera123@192.168.10.51/ONVIF/MediaInput/h264", type=str)
parser.add_argument("--videofile", default="/home/aj1m0n/MOT/data/C0133-480p.mp4", type=str)
parser.add_argument("--json_path", default='/home/aj1m0n/MOT/data/json/', type=str)
```
To change target file:
```
python3 main.py --videofile /workspace/data/C0133_v4.mp4
```


### Deep SORT with low confidence track filtering
This version has the option to hide object detections instead of tracking. The settings in `main.py` are
```
show_detections = True
writeVideo_flag = True
asyncVideo_flag = False
```

Setting `show_detections = False` will hide object detections and show the average detection confidence and the most commonly detected class for each track.

To modify the average detection threshold, go to `deep_sort/tracker.py` and change the `adc_threshold` argument on line 40. You can also change the number of steps that the detection confidence will be averaged over by changing `n_init` here.

# Training your own models
## YOLO v4
See https://github.com/Ma-Dan/keras-yolo4.

## Deep SORT
Please note that the tracking model used here is only trained on tracking people, so you'd need to train a model yourself for tracking other objects.

See https://github.com/nwojke/cosine_metric_learning for more details on training your own tracking model.

For those that want to train their own **vehicle** tracking model, I've created a tool for converting the [DETRAC](http://detrac-db.rit.albany.edu/) dataset into a trainable format for cosine metric learning and can be found in my object tracking repository [here](https://github.com/LeonLok/Multi-Camera-Live-Object-Tracking/tree/master/detrac_tools). The tool was created using the earlier mentioned [paper](https://ieeexplore.ieee.org/document/8909903) as reference with the same parameters.

## Automatic startup
```
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

docker run -it -v ~/workspace/:/workspace/ --runtime nvidia --network host aj1m0n/deep_sort:latest
```