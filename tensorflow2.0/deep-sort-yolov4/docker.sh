sudo docker run -it -v ~/workspace/:/workspace/ --device /dev/video0:/dev/video0 --runtime nvidia --network host aj1m0n/deep_sort:latest 
