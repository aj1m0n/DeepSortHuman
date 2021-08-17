import json

class CountParson:
    def __init__(self):
        self.parson_id_list = []
        self.first_position_list = []
        self.end_position_list = []
        self.first_id_list = []
        self.count_list = []
        self.t_count_list = []
        self.f_count_list = []
        self.ids_position_dict = {}
        self.path = "./json/"
        

    def positions(self, _parson_dict, _latest_track_id):
        _latest_track_id = int(_latest_track_id)
        print(_latest_track_id)
        if len(_parson_dict) == 0:
            return len(self.t_count_list), len(self.f_count_list)
        print(_parson_dict)
        if  len(self.first_id_list) == 0:
            self.first_id_list.append(_latest_track_id)
            self.first_position_list.append(_parson_dict[str(_latest_track_id)])

        if  not _latest_track_id in self.first_id_list:
            self.first_id_list.append(_latest_track_id)
            self.first_position_list.append(_parson_dict[str(_latest_track_id)])

        for _track_id in self.first_id_list:
            print('positions')
            if not _parson_dict.get(str(_track_id)):
                if self.first_position_list[int(_track_id)-1][0] - self.end_position_list[int(_track_id)-1][0] > 0:
                    self.t_count_list.append(int(_track_id))
                    self.ids_position_dict["direction"] = "R"

                else:
                    self.f_count_list.append(int(_track_id))
                    self.ids_position_dict["direction"] = "L"
                self.ids_position_dict["id"] = _track_id
                self.ids_position_dict["1st_position"] = self.first_position_list[int(_track_id) -1]
                self.ids_position_dict["end_position"] = self.end_position_list[int(_track_id) -1]
                self.create_dummy_data(_track_id)
                self.first_id_list.remove(_track_id)
            else:
                self.end_position_list.append(_parson_dict[str(_track_id)])
        return len(self.t_count_list), len(self.f_count_list)

    def create_dummy_data(self, _i):
        with open(self.path + str(_i) + '.json', mode='w', encoding='utf-8') as _file:
            json.dump(self.ids_position_dict , _file, ensure_ascii=False, indent = 2)

        return True