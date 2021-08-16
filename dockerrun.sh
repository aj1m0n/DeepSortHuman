docker run -it -v ~/workspace/DeepSortHuman/:/DeepSortHuman/ --device /dev/video0:/dev/video0 --restart=always --runtime nvidia --network host --name deepsort deepsort:human
