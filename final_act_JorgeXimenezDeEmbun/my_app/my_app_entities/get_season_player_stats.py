import requests


class GetSeasonPlayerStats:

    def __init__(self, base_url, player_id, player_season):
        self.__base_url = base_url
        self.__endpoint_url = '/stats'
        self.__player_id = player_id
        self.__seasons = player_season
        self.__season_player_stats = {}
    
    
    def get_season_player_stats (self):

        params = {
            'player_ids[]' : [self.__player_id], 
            'seasons[]' : [self.__seasons],
            'per_page' : 100,
        }

        response = requests.get(self.__base_url+self.__endpoint_url, params=params)
        response_json = response.json()

        for game in range(len(response_json['data'])):
            player_stats = {}
            player_stats['game_ID'] = response_json['data'][game]['game']['id']
            player_stats['player_team_ID'] = response_json['data'][game]['team']['id']
            player_stats['min'] = self.__null_stats(response_json['data'][game]['min'])
            player_stats['pts'] = self.__null_stats(response_json['data'][game]['pts'])
            player_stats['fg3a'] = self.__null_stats(response_json['data'][game]['fg3a'])
            player_stats['fg3m'] = self.__null_stats(response_json['data'][game]['fg3m'])
            player_stats['fg2a'] = self.__null_stats(response_json['data'][game]['fga']) - player_stats['fg3a']
            player_stats['fg2m'] = self.__null_stats(response_json['data'][game]['fgm']) - player_stats['fg3m']
            player_stats['fta'] = self.__null_stats(response_json['data'][game]['fta'])
            player_stats['ftm'] = self.__null_stats(response_json['data'][game]['ftm'])
            player_stats['ast'] = self.__null_stats(response_json['data'][game]['ast'])
            player_stats['stl'] = self.__null_stats(response_json['data'][game]['stl'])
            player_stats['turnover'] = self.__null_stats(response_json['data'][game]['turnover'])
            player_stats['reb'] = self.__null_stats(response_json['data'][game]['reb'])
            player_stats['dreb'] = self.__null_stats(response_json['data'][game]['dreb'])
            player_stats['oreb'] = self.__null_stats(response_json['data'][game]['oreb'])
            player_stats['blk'] = self.__null_stats(response_json['data'][game]['blk'])
            player_stats['pf'] = self.__null_stats(response_json['data'][game]['pf'])

            game_ID = player_stats['game_ID']
            self.__season_player_stats[game_ID] = player_stats

        if self.__season_player_stats:
            return(self.__season_player_stats, True)
        else:
            return(self.__season_player_stats, False)

    
    def __null_stats (self, value):
        self.value = value

        if self.value is None:
            return (0)
        else:
            return (self.value)