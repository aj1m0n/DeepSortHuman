import json
import collections as cl
from timeit import time
import pika

def create_jsondata(_camera_ip, _date, _dt, _car_data, _create_json_flag, _json_path, _i):
    _data = {}
    _data["IP"] = _camera_ip,
    _data["date"] = _date,
    _data["data"] = _car_data
    _data["dt"] = _dt
    if _create_json_flag:
        create_dummy_data(_data, _json_path, _i) 
    return json.dumps(_data)

def create_dummy_data(_data, _path, _i):
    with open(_path + str(_i) + '.json', mode='w', encoding='utf-8') as _file:
        json.dump(_data, _file, ensure_ascii=False, indent = 2)

    return True

def send_amqp(_json_data, _key, _host):
    _connection = pika.BlockingConnection(pika.ConnectionParameters(host=_host))
    _channel = _connection.channel()
    _channel.exchange_declare(exchange='signal', exchange_type='topic')
    _json_command = str(_json_data)
    _channel.basic_publish(exchange='signal',routing_key=_key, body=_json_command)
    print("Sent: {} Routing Key: {}".format(_json_command, _key))

if __name__ == "__main__":
    import datetime
    nowtime = datetime.datetime.now().isoformat()