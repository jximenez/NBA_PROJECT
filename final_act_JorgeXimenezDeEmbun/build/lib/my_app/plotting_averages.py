import matplotlib.pyplot as plt
import json


class StatsPlot:

    def __init__(self, player_name, player_seasons_list):

        self.__player_name = player_name
        self.__player_seasons = player_seasons_list
        self.__points_dic = {}
        self.__games_dic = {}
        self.__mins_dic = {}
        self.__ast_dic = {}
        self.__steal_dic = {}
    

    def __get_dic(self):
        
        for season in self.__player_seasons:
            try:
                with open(f'my_app/my_app_saved_files/average_season_stats/{self.__player_name}_{season}_AverageStats.json', 'r') as season_average_file:
                    player_stats = json.load(season_average_file)
                    player_points = player_stats['pts']
                    player_games = player_stats['games_played']
                    player_mins = player_stats['min']
                    player_ast = player_stats['ast']
                    player_steal = player_stats['stl']
            
                self.__points_dic[season] = player_points
                self.__games_dic[season] = player_games
                self.__mins_dic[season] = player_mins
                self.__ast_dic[season] = player_ast
                self.__steal_dic[season] = player_steal

            except FileNotFoundError:
                print('No se ha podido descargar la grafica correctamente o se ha movido de ubicacion')
        

    def draw_points_plot(self):
        
        self.__get_dic()
        xAxis = [season for season, points in self.__points_dic.items()]
        yAxis = [points for season, points in self.__points_dic.items()]
        plt.grid(True)

        plt.plot(xAxis, yAxis, color='maroon', marker='o')
        plt.xlabel('Seasons')
        plt.ylabel('Points')
        
        plt.title(f'Career points {self.__player_name}')
        plt.savefig(f'my_app/my_app_saved_files/plots/{self.__player_name}_average_points.jpg')
        plt.show()
    
    def draw_games_plot(self):
        
        self.__get_dic()
        xAxis = [season for season, games in self.__games_dic.items()]
        yAxis = [games for season, games in self.__games_dic.items()]
        plt.grid(True)

        plt.plot(xAxis, yAxis, color='maroon', marker='o')
        plt.xlabel('Seasons')
        plt.ylabel('Games played')
        
        plt.title(f'Career games played {self.__player_name}')
        plt.savefig(f'my_app/my_app_saved_files/plots/{self.__player_name}_average_games_played.jpg')
        plt.show()

    def draw_mins_plot(self):
        
        self.__get_dic()
        xAxis = [season for season, mins in self.__mins_dic.items()]
        yAxis = [mins for season, mins in self.__mins_dic.items()]
        plt.grid(True)

        plt.plot(xAxis, yAxis, color='maroon', marker='o')
        plt.xlabel('Seasons')
        plt.ylabel('Minutes played')
        
        plt.title(f'Career minutes played {self.__player_name}')
        plt.savefig(f'my_app/my_app_saved_files/plots/{self.__player_name}_average_minutes_played.jpg')
        plt.show()

    def draw_ast_plot(self):
        
        self.__get_dic()
        xAxis = [season for season, ast in self.__ast_dic.items()]
        yAxis = [ast for season, ast in self.__ast_dic.items()]
        plt.grid(True)

        plt.plot(xAxis, yAxis, color='maroon', marker='o')
        plt.xlabel('Seasons')
        plt.ylabel('Assistances')
        
        plt.title(f'Career assistances {self.__player_name}')
        plt.savefig(f'my_app/my_app_saved_files/plots/{self.__player_name}_average_assistances.jpg')
        plt.show()

    def draw_steal_plot(self):
        
        self.__get_dic()
        xAxis = [season for season, steal in self.__steal_dic.items()]
        yAxis = [steal for season, steal in self.__steal_dic.items()]
        plt.grid(True)

        plt.plot(xAxis, yAxis, color='maroon', marker='o')
        plt.xlabel('Seasons')
        plt.ylabel('Steals')
        
        plt.title(f'Career steals {self.__player_name}')
        plt.savefig(f'my_app/my_app_saved_files/plots/{self.__player_name}_average_steals.jpg')
        plt.show()
    
