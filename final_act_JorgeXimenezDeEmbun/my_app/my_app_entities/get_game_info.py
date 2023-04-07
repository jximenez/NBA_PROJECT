import requests


class GetGameInfo:

    def __init__(self, base_url, game_id):
        self.__base_url = base_url
        self.__endpoint_url = '/games/'
        self.__game_id = game_id
        self.__game_info = {}

    def get_game_info(self):

        response = requests.get(self.__base_url+self.__endpoint_url+self.__game_id)
        response_json = response.json()

        self.__game_info['date'] = response_json['date']
        self.__game_info['status'] = response_json['status']
        self.__game_info['home_team_score'] = response_json['home_team_score']
        self.__game_info['visitor_team_score'] = response_json['visitor_team_score']
        self.__game_info['home_team_id'] = response_json['home_team']['id']
        self.__game_info['home_team_full_name'] = response_json['home_team']['full_name']
        self.__game_info['visitor_team_id'] = response_json['visitor_team']['id']
        self.__game_info['visitor_team_full_name'] = response_json['visitor_team']['full_name']
        
        if self.__game_info:
            return (self.__game_info, True)
        else:
            return (self.__game_info, False)


