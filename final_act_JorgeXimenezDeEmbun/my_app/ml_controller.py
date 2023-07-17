import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
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
        df_games_played = pd.read_sql_query(f'SELECT * from PARTIDOS_DISPUTADOS WHERE IDJugador = {player_id}', self.__connection)  
        transform_data = MlTransformData(df_player_stats, df_games_stats, df_games_played)
        data = transform_data.transform_data()
        train_model = MlTrainModel(data)
        class_model, reg_model = train_model.train_model()
        return (class_model, reg_model)

    def prediction (self, class_model, reg_model, stats):
        self.__class_model = class_model
        self.__reg_model = reg_model
        self.__stats = stats

        feature_cols = ['Minutos','Puntos','Asistencias','Robos','Perdidas','Tapones','Faltas','Rebotes']
        features = pd.DataFrame(np.array([self.__stats]), columns=feature_cols)

        class_prediction = self.__class_model.predict(features)  
        reg_prediction = self.__reg_model.predict(features) 
        
        return class_prediction, reg_prediction

    

    