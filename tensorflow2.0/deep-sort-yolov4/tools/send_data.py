import json
import collections as cl


def create_data(_camera_ip, _car_id_list, _position_list, _daytime):
    _data = cl.OrderedDict()
    _data["IP"] = _camera_ip,
    _data["date"] = _daytime,
    _data["data"] = cl.OrderedDict(zip(_car_id_list, _position_list))
 
    return json.dumps(_data)

if __name__ == "__main__":
    import datetime
    nowtime = datetime.datetime.now().isoformat()
    print(create_data('192.168.1.1', ['1', '2', '3'], [[100,100,100,100], [200,200,200,200], [300,300,300,300]], nowtime))
