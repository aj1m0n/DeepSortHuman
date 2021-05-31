import json
import collections as cl


def create_jsondata(_camera_ip, _date, _car_data):
    _data = cl.OrderedDict()
    _data["IP"] = _camera_ip,
    _data["date"] = _date,
    _data["data"] = cl.OrderedDict(_car_data)
 
    return json.dumps(_data)

def create_dummy_data(_jsondata):
    _json_dict = json.load(_jsondata)
    

if __name__ == "__main__":
    import datetime
    nowtime = datetime.datetime.now().isoformat()
    print(create_data('192.168.1.1', ['1', '2', '3'], [[100,100,100,100], [200,200,200,200], [300,300,300,300]], nowtime))
