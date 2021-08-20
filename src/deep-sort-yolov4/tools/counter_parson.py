import json
import math
import copy

class CountParson:
    def __init__(self):
        self.first_position_list = {}
        self.end_position_list = {}
        self.t_count_list = []
        self.f_count_list = []
        self.ids_position_dict = {}
        self.path = "../../../DemoSortServer/data/json/"
        

    def positions(self, _parson_dict, _latest_track_id, _date):
        _latest_track_id = int(_latest_track_id)
        if len(_parson_dict) == 0 and len(self.first_position_list) == 0:
            return len(self.t_count_list), len(self.f_count_list)
        
        if  len(self.first_position_list) == 0:
            self.first_position_list = _parson_dict
            
        _new_keys_dict = _parson_dict.keys() - self.first_position_list.keys()
        _intersection_keys_dict = _parson_dict.keys() & self.first_position_list.keys()
        
        if len(_intersection_keys_dict) > 0:
            for _key in _intersection_keys_dict:
                self.end_position_list[_key] = _parson_dict[_key]
        
        if  len(_new_keys_dict) > 0:
            for _key in _new_keys_dict:
                self.first_position_list[_key] = _parson_dict[_key]
        
        _ftemp = copy.copy(self.first_position_list)
        _etemp = copy.copy(self.end_position_list)
        for _key in self.end_position_list.keys():
            if not _key in _parson_dict.keys():
                _fx = int(self.first_position_list[_key][0] + (self.first_position_list[_key][2] - self.first_position_list[_key][0]) / 2)
                _fy = int(self.first_position_list[_key][1] + (self.first_position_list[_key][3] - self.first_position_list[_key][1]) / 2)
                _ex = int(self.end_position_list[_key][0] + (self.end_position_list[_key][2] - self.end_position_list[_key][0]) / 2)
                _ey = int(self.end_position_list[_key][1] + (self.end_position_list[_key][3] - self.end_position_list[_key][1]) / 2)
                if math.sqrt(pow(_ex -_fx, 2) + pow(_ey - _fy, 2)) > 250:
                    self.ids_position_dict["id"] = _key
                    if _ex -_fx > 0:
                        self.ids_position_dict["direction"] = "L"
                        self.t_count_list.append(_key)
                    else:
                        self.ids_position_dict["direction"] = "R" 
                        self.f_count_list.append(_key)

                    self.ids_position_dict["date"] = _date
                    self.ids_position_dict["1st_position"] = self.first_position_list[_key]
                    self.ids_position_dict["end_position"] = self.end_position_list[_key]
                    print(self.ids_position_dict)
                    self.create_dummy_data(_key)
                    self.ids_position_dict.clear()
                _ftemp = copy.copy(_ftemp.pop(_key))
                _etemp = copy.copy(_etemp.pop(_key))
            else:
                _etemp[_key] =  _parson_dict[_key]
        self.first_position_list = _ftemp
        self.end_position_list = _etemp
        return len(self.t_count_list), len(self.f_count_list)

    def create_dummy_data(self, _i):
        with open(self.path + str(_i) + '.json', mode='w', encoding='utf-8') as _file:
            json.dump(self.ids_position_dict , _file, ensure_ascii=False, indent = 2)

        return True
