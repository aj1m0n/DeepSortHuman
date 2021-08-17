class CountParson:
    def __init__(self):
        self.parson_id_list = []
        self.first_position_list = []
        self.end_position_list = []
        self.first_id_list = [0]
        self.count_list = []
        self.t_count_list = []
        self.f_count_list = []
        

    def positions(self, _parson_dict, _latest_track_id):
        print(_latest_track_id)
        if  _latest_track_id > len(self.first_id_list) - 1:
            self.first_id_list.append(_latest_track_id)
            self.first_position_list[_latest_track_id] = _parson_dict[str(_latest_track_id)]

        for _track_id in self.first_id_list:
            print('positions')
            if not _parson_dict.get(str(_track_id)):
                if self.first_position_list[int(_track_id)][0] - self.end_position_list[int(_track_id)][0] > 0:
                    self.t_count_list.append(int(_track_id))
                else:
                    self.f_count_list.append(int(_track_id))
            else:
                self.end_position_list[int(_track_id)] = _parson_dict[str(_track_id)]
        
        return len(self.t_count_list), len(self.f_count_list)

    

