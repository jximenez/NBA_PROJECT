import requests

class GetAveragePlayerStats:

    def __init__(self, base_url, player_id, player_season):
        self.__base_url = base_url
        self.__endpoint_url = '/season_averages'
        self.__player_id = player_id
        self.__seasons = player_season
        self.__average_player_stats = {}
    
    
    def get_average_player_stats (self):

        params = {
            'player_ids[]' : [self.__player_id], 
            'season' : self.__seasons,
        }

        response = requests.get(self.__base_url+self.__endpoint_url, params=params)
        response_json = response.json()

        try:
            self.__average_player_stats['games_played'] = response_json['data'][0]['games_played']
            self.__average_player_stats['season'] = response_json['data'][0]['season']
            self.__average_player_stats['min'] = self.__null_stats(response_json['data'][0]['min'])            
            self.__average_player_stats['pts'] = self.__null_stats(response_json['data'][0]['pts'])
            self.__average_player_stats['fg3a'] = self.__null_stats(response_json['data'][0]['fg3a'])
            self.__average_player_stats['fg3m'] = self.__null_stats(response_json['data'][0]['fg3m'])
            self.__average_player_stats['fg2a'] = self.__null_stats(response_json['data'][0]['fga']) - self.__average_player_stats['fg3a']
            self.__average_player_stats['fg2m'] = self.__null_stats(response_json['data'][0]['fgm']) - self.__average_player_stats['fg3m']
            self.__average_player_stats['fta'] = self.__null_stats(response_json['data'][0]['fta'])
            self.__average_player_stats['ftm'] = self.__null_stats(response_json['data'][0]['ftm'])
            self.__average_player_stats['ast'] = self.__null_stats(response_json['data'][0]['ast'])
            self.__average_player_stats['stl'] = self.__null_stats(response_json['data'][0]['stl'])
            self.__average_player_stats['turnover'] = self.__null_stats(response_json['data'][0]['turnover'])
            self.__average_player_stats['reb'] = self.__null_stats(response_json['data'][0]['reb'])
            self.__average_player_stats['dreb'] = self.__null_stats(response_json['data'][0]['dreb'])
            self.__average_player_stats['oreb'] = self.__null_stats(response_json['data'][0]['oreb'])
            self.__average_player_stats['blk'] = self.__null_stats(response_json['data'][0]['blk'])
            self.__average_player_stats['pf'] = self.__null_stats(response_json['data'][0]['pf'])

            return(self.__average_player_stats, True)
        
        except IndexError:
            return(self.__average_player_stats, False)

    
    def __null_stats (self, value):
        self.value = value

        if self.value is None:
            return (0)
        else:
            return (self.value)