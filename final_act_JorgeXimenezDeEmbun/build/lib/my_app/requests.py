import json

from my_app.my_app_entities.get_season_player_stats import GetSeasonPlayerStats
from my_app.my_app_entities.get_players_id import GetPlayersId
from my_app.my_app_entities.get_game_info import GetGameInfo
from my_app.my_app_entities.get_average_player_stats import GetAveragePlayerStats


class Requests:

    def __init__(self, player_name, season, game_id):
        
        self.__base_url = 'https://www.balldontlie.io/api/v1'
        self.__player_name = player_name
        self.__player_season = str(season)
        self.__game_id = str(game_id)
    
    def getting_player_id(self):
        get_players_id = GetPlayersId(self.__base_url, self.__player_name)
        player_info, does_exist = get_players_id.get_players_id()
        if does_exist:
            with open(f'my_app/my_app_saved_files/players_requested/{self.__player_name}.json', 'w') as json_player_file:
                json.dump(player_info, json_player_file)
            return (True)

        elif player_info == 0:
            print(f'Player {self.__player_name} does not exit in the NBA history')
            return(False)
        elif player_info > 1:
            print(f'We found {player_info} players with the same name; {self.__player_name}, in the NBA history, try to be more specific')
            return(False)


    def getting_players_stats(self):

        with open(f'my_app/my_app_saved_files/players_requested/{self.__player_name}.json', 'r') as player_file:
            player_info = json.load(player_file)
            player_id = player_info['id']

        get_players_stats = GetSeasonPlayerStats(self.__base_url, player_id, self.__player_season)
        player_season_stats, season_played = get_players_stats.get_season_player_stats()
        if season_played:
            with open(f'my_app/my_app_saved_files/stats_players_requested/{self.__player_name}_{self.__player_season}.json', 'w') as json_stats_file:
                json.dump(player_season_stats, json_stats_file)
        else:
            print(f'Season {self.__player_season} not played by {self.__player_name}')


    def getting_game_info(self):
        
        with open(f'my_app/my_app_saved_files/stats_players_requested/{self.__player_name}_{self.__player_season}.json', 'r') as season_stats_file:
                season_stats = json.load(season_stats_file)
        
        if self.__game_id in season_stats:
            get_game_info = GetGameInfo(self.__base_url, self.__game_id)
            game_info, exist = get_game_info.get_game_info()

            if exist:
                with open(f'my_app/my_app_saved_files/games_info/{self.__player_name}_{self.__player_season}_{self.__game_id}.json', 'w') as games_info_file:
                        json.dump(game_info, games_info_file)
            else:
                print(f'Game {self.__game_id} does exist in season {self.__player_season} but we have no info')
        
        else:
            print(f'Game {self.__game_id} not in season {self.__player_season}')


    def getting_average_season_player_stats(self):
        
        with open(f'my_app/my_app_saved_files/players_requested/{self.__player_name}.json', 'r') as player_file:
                player_info = json.load(player_file)
                player_id = player_info['id']

        get_average_player_stats = GetAveragePlayerStats(self.__base_url, player_id, self.__player_season)
        average_stats, exist = get_average_player_stats.get_average_player_stats()
        if exist:
            with open(f'my_app/my_app_saved_files/average_season_stats/{self.__player_name}_{self.__player_season}_AverageStats.json', 'w') as average_stats_file:
                        json.dump(average_stats, average_stats_file)
        else:
            print(f'{self.__player_name} average stats for season {self.__player_season} not found')
