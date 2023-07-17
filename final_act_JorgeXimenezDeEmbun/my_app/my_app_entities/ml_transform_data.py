import pandas as pd
import numpy as np

class MlTransformData:
    def __init__(self, df_player_stats, df_games_stats, df_games_played):
        self.__df_player_stats = df_player_stats
        self.__df_games_stats = df_games_stats
        self.__df_games_played = df_games_played
    
    def __add_results(self, dataframe):
        for row in list(range(len(dataframe))):
            if (dataframe['IDEquipo jugador'][row] == dataframe['IDEquipo local'][row]) and (dataframe['Puntos equipo local'][row] > dataframe['Puntos equipo visitante'][row]):
                dataframe['Puntos diferencia'][row] = dataframe['Puntos equipo local'][row] - dataframe['Puntos equipo visitante'][row]
            else: 
                if (dataframe['IDEquipo jugador'][row] == dataframe['IDEquipo visitante'][row]) and (dataframe['Puntos equipo visitante'][row] > dataframe['Puntos equipo local'][row]):
                    dataframe['Resultado'][row] = 'G'
                    dataframe['Puntos diferencia'][row] = dataframe['Puntos equipo visitante'][row] - dataframe['Puntos equipo local'][row]

                else:
                    dataframe['Resultado'][row] = 'P'
                    if dataframe['Puntos equipo visitante'][row] > dataframe['Puntos equipo local'][row]:
                        dataframe['Puntos diferencia'][row] = dataframe['Puntos equipo local'][row] - dataframe['Puntos equipo visitante'][row]
                    else: dataframe['Puntos diferencia'][row] = dataframe['Puntos equipo visitante'][row] - dataframe['Puntos equipo local'][row]
        return dataframe

    def __drop_columns(self, data, columns):
        '''
        Función que elimina dado un dataframe las columnas indicadas en una lista
        Input:
            - data: pandas dataframe
            - columns: lista
        Output: pandas dataframe
        '''
        data.drop(columns, axis=1, inplace=True)
        return
    
    def __minutes_to_number(self, data):
        '''
        Función para transformar la columna Minutos de tipo object a tipo int
        Input: pandas dataframe
        Output: pandas dataframe
        '''
        data['Minutos'] = data['Minutos'].apply(lambda x: np.nan if x == '' else float(x.split(':')[0]))
        return


    def transform_data(self):
        df_merge_games_stats = pd.merge(left=self.__df_games_played, right=self.__df_games_stats, how='inner', on=['IDPartido'])
        self.__df_player_stats['Rebotes'] = self.__df_player_stats['Rebotes ofensivos'] + self.__df_player_stats['Rebotes defensivos']
        df_merge_games_stats['Resultado'] = np.nan
        df_merge_games_stats['Puntos diferencia'] = np.nan
        self.__add_results(df_merge_games_stats)
        columns_to_drop = ['IDEquipo jugador', 'Temporada', 'Fecha', 'IDEquipo local', 'Nombre equipo local', 'Puntos equipo local', 'IDEquipo visitante', 'Nombre equipo visitante', 'Puntos equipo visitante']
        self.__drop_columns(df_merge_games_stats, columns_to_drop)
        df_merge_player_stats = pd.merge(left=self.__df_player_stats, right=df_merge_games_stats, how='inner', on=['IDJugador','IDPartido'])
        self.__minutes_to_number(df_merge_player_stats)
        df_merge_player_stats.interpolate(method='linear', limit_direction='forward', axis=0, inplace=True)
        columns_to_drop = ['IDPartido', 'IDJugador', 'Tiros 3 intentados','Tiros 3 conseguidos', 'Tiros 2 intentados','Tiros 2 conseguidos','Tiros libres intentados', 'Tiros libres conseguidos', 'Rebotes ofensivos', 'Rebotes defensivos']
        self.__drop_columns(df_merge_player_stats, columns_to_drop)
        return(df_merge_player_stats)



