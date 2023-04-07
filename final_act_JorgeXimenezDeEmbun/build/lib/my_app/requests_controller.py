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
                requests.getting_players_stats()
            else:
                print('Try again with a diferent name')
                break 

    def downloading_game_info(self):

        for season in self.__player_season_list:
            requests = Requests(self.__player_name, season, self.__game_id)
            requests.getting_game_info()

    def downloading_average_season_player_stats(self):

        for season in self.__player_season_list:
            requests = Requests(self.__player_name, season, self.__game_id)
            player_exist = requests.getting_player_id()
            if player_exist:
                requests.getting_average_season_player_stats()
            
    def drawing_average_plot(self, plot_type):
        
        stats_plot = StatsPlot(self.__player_name, self.__player_season_list)
        if plot_type == '1':
            stats_plot.draw_games_plot()
        if plot_type == '2':
            stats_plot.draw_mins_plot()
        if plot_type == '3':
            stats_plot.draw_points_plot()
        if plot_type == '4':
            stats_plot.draw_ast_plot()
        if plot_type == '5':
            stats_plot.draw_steal_plot()
