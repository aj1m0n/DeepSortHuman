docker run -it -v ~/workspace/Deep_Sort/:/Deep_Sort/ -e IP=`ip -f inet -o addr show wlan0|cut -d\  -f 7 | cut -d/ -f 1` --runtime nvidia --network host --name deepsort deepsort
