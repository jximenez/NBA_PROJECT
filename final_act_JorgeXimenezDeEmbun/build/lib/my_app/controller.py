from my_app.requests import Requests
from my_app.plotting_averages import StatsPlot


class Controller:

    def __init__(self, player_name, season_played, game_id):
        self.__player_name = player_name
        self.__player_season_list = season_played
        self.__game_id = game_id


    def downloading_players_info(self):
    
        for season in self.__player_season_list:
            requests = Requests(self.__player_name, season, self.__game_id)
            player_exist = requests.getting_player_id()
            if player_exist:
                #requests.getting_average_season_player_stats()
                requests.getting_players_stats()
                
            else:
                print('Try again with a diferent name')
                break
        
        #if player_exist:
            #stats_plot = StatsPlot(self.__player_name, self.__player_season_list)
            #stats_plot.draw_points_plot() 
    

    def downloading_game_info(self):

        for season in self.__player_season_list:
            requests = Requests(self.__player_name, season, self.__game_id)
            requests.getting_game_info()



