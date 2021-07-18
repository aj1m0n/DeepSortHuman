IP=`ip -f inet -o addr show eth0|cut -d\  -f 7 | cut -d/ -f 1`
python3 ./main.py --key 'jp.chiba.kashiwa.kashiwanoha.25.sensor.' --ipaddress $IP  -ipcamera_flag