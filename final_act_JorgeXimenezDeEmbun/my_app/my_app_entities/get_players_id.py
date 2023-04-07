import requests


class GetPlayersId:

    def __init__(self, base_url, player_name):
        self.__base_url = base_url
        self.__endpoint_url = '/players'
        self.__player_name = player_name
        self.__players_info = {}


    def get_players_id(self):

        params = {
            'search' : f'{self.__player_name}'
        }

        response = requests.get(self.__base_url+self.__endpoint_url, params=params)
        response_json = response.json()
        total_count = response_json['meta']['total_count']
        
        if total_count == 0:
            players_found = response_json['meta']['total_count']
            return(players_found, False)
        elif total_count > 1:
            players_found = response_json['meta']['total_count']
            return(players_found, False)
        elif total_count == 1:
            self.__players_info = response_json['data'][0]
            return(self.__players_info, True)
        
        
    

   

        



        
