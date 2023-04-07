import matplotlib.pyplot as plt
import json


class StatsPlot:

    def __init__(self, player_name, player_seasons_list):

        self.__player_name = player_name
        self.__player_seasons = player_seasons_list
        self.__points_dic = {}
    

    def __get_points_dic(self):
        
        for season in self.__player_seasons:
            try:
                with open(f'my_app/my_app_saved_files/average_season_stats/{self.__player_name}_{season}_AverageStats.json', 'r') as season_average_file:
                    player_stats = json.load(season_average_file)
                    player_points = player_stats['pts']
            
                self.__points_dic[season] = player_points

            except FileNotFoundError:
                continue
        
        return (self.__points_dic)

    def draw_points_plot(self):

        points_dic = self.__get_points_dic()
        xAxis = [season for season, points in points_dic.items()]
        yAxis = [points for season, points in points_dic.items()]
        plt.grid(True)

        plt.plot(xAxis, yAxis, color='maroon', marker='o')
        plt.xlabel('Seasons')
        plt.ylabel('Points')
        
        plt.title(f'Career points {self.__player_name}')
        plt.savefig(f'my_app/my_app_saved_files/plots/{self.__player_name}_average_points.jpg')
    
       

    
