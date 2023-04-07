import pandas as pd
from my_app.my_app_entities.ml_transform_data import MlTransformData
from my_app.my_app_entities.ml_train_model import MlTrainModel


class Mlcontroller:

    def __init__(self, connection):
        self.__connection = connection

    def show_players_in_database(self):
        df_players = pd.read_sql_query('SELECT * from JUGADORES', self.__connection)
        return(df_players)
    
    def trainning_model(self):
        player_id = int(input('Introduce el ID del jugador: '))
        df_player_stats = pd.read_sql_query(f'SELECT * from ESTADISTICAS_PARTIDO_JUGADORES WHERE IDJugador = {player_id}', self.__connection)
        df_games_stats = pd.read_sql_query('SELECT * from PARTIDOS', self.__connection)
        transform_data = MlTransformData(df_player_stats, df_games_stats)
        data = transform_data.transform_data()
        train_model = MlTrainModel(data)
        model = train_model.train_model()
        return model

    def prediction (self, model, stats):
        self.__model = model
        self.__stats = stats
        pass

    

    