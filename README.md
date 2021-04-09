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

All tests were done using an Nvidia Xavier NX.

However,using webcamera is much slower than reading video.(~2.0fps)

# Quick start
[Download](https://drive.google.com/open?id=1cewMfusmPjYWbrnuJRuKhPMwRe_b9PaT) and convert the Darknet YOLO v4 model  to a Keras model by modifying `convert.py` accordingly and run:
```
python convert.py
```
Then run main.py:
```
python main.py
```

## Settings

### Normal Deep SORT
By default, tracking and video writing is on and asynchronous processing is off. These can be edited in `demo.py` by changing:
```
tracking = True
writeVideo_flag = True
asyncVideo_flag = False
```

To change target file in `demo.py`:
```
file_path = 'video.webm'
```

To change output settings in `demo.py`:
```
out = cv2.VideoWriter('output_yolov4.avi', fourcc, 30, (w, h))
```

### Deep SORT with low confidence track filtering
This version has the option to hide object detections instead of tracking. The settings in `demo.py` are
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

# Dependencies
* Tensorflow GPU 1.14
* Keras 2.3.1
* opencv-python 4.2.0
* imutils 0.5.3
* numpy 1.18.2
* sklearn

## Running with Tensorflow 1.14 vs 2.0
Navigate to the appropriate folder and run python scripts. 

### Conda environment used for Tensorflow 2.0
(see requirements.txt)
* imutils                   0.5.3                    
* keras                     2.3.1                    
* matplotlib                3.2.1                    
* numpy                     1.18.4                   
* opencv-python             4.2.0.34                 
* pillow                    7.1.2                    
* python                    3.6.10               
* scikit-learn              0.23.1                   
* scipy                     1.4.1                    
* sklearn                   0.19                     
* tensorboard               2.2.1                    
* tensorflow                2.0.0                    
* tensorflow-estimator      2.1.0                    
* tensorflow-gpu            2.2.0                    
