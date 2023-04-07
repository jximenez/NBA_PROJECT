import pandas as pd
import numpy as np

class MlTransformData:
    def __init__(self, df_player_stats, df_games_stats):
        self.__df_player_stats = df_player_stats
        self.__df_games_stats = df_games_stats
    

    def transform_data(self):
        pass