sudo docker run -it -v /home/jetson-iwai/workspace/:/workspace/ --device /dev/video0:/dev/video0 --runtime nvidia --network host jetson-iwai/l4-ml-ten2:v2.0
