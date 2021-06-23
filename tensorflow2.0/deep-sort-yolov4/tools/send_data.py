import json
import collections as cl
from timeit import time


def create_jsondata(_camera_ip, _date, _car_data, _create_json_flag, _json_path, _i):
    _data = cl.OrderedDict()
    _data["IP"] = _camera_ip,
    _data["date"] = _date,
    _data["data"] = cl.OrderedDict(_car_data)
    if _create_json_flag:
        create_dummy_data(_data, _json_path, _i)
    
    return json.dumps(_data)

def create_dummy_data(_data, _path, _i):
    _data["date"] = (_i + 1) / 3 
    with open(_path + str(_i) + '.json', mode='w', encoding='utf-8') as _file:
        json.dump(_data, _file, ensure_ascii=False, indent = 2)

    return True


if __name__ == "__main__":
    import datetime
    nowtime = datetime.datetime.now().isoformat()