import sqlite3
from sqlite3 import Error
import json
from time import sleep
from random import randint
from my_app.requests_controller import Controller


def execute_query(connection, query, first_message):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        if first_message:
            print("""
                ** Puede que la descarga tarde poco mas de 1 minuto, 
                esperar a que vuelva a aparecer el menu de inicio **
                """)
    except Error as e:
        print(f"Error: '{e}'")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        print('** DATOS EXISTENTES **')
        column_names = [description[0] for description in cursor.description]
        print(column_names)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Error: '{e}'")


class Dbcontroller:

    def __init__(self, connection):
        self.__connection = connection

    def add_player_stats_in_db(self):

        player_name_2 = str(input('Inserte el nombre y 1er apellido del jugador: '))
        seasons_list_2 = []
        season_played_2 = int(input('Inserte la temporada: '))
        seasons_list_2.append(season_played_2)
        controller_2 = Controller(player_name_2, seasons_list_2,0)
        controller_2.downloading_players_info()
        try:
            with open(f'my_app/my_app_saved_files/players_requested/{player_name_2}.json', 'r') as player_file:
                player_info = json.load(player_file)
            player_id = player_info['id']
            player_name = player_info['first_name'] + ' ' + player_info['last_name']
            player_position = player_info['position']
            player_height = player_info['height_feet']
            player_weight = player_info['weight_pounds']
            qry_insert_player = f"""INSERT INTO JUGADORES (IDJugador, Nombre, Posicion,Altura,Peso) SELECT '{player_id}' , '{player_name}' , '{player_position}' , '{player_height}' , '{player_weight}' WHERE NOT EXISTS (SELECT 1 FROM JUGADORES WHERE IDJugador= '{player_id}')"""
            execute_query(self.__connection, qry_insert_player, True)  

            with open(f'my_app/my_app_saved_files/stats_players_requested/{player_name_2}_{season_played_2}.json', 'r') as stats_player_file:
                season_player_stats = json.load(stats_player_file)
            for game in season_player_stats.keys():
                sleep(randint(1,2))       #Balldontie API has Rate limit of 60 requests per minute
                controller_3 = Controller(player_name_2, seasons_list_2, game)
                controller_3.downloading_game_info()
                with open(f'my_app/my_app_saved_files/games_info/{player_name_2}_{season_played_2}_{game}.json', 'r') as stats_game_file:
                    player_season_game = json.load(stats_game_file)
                game_id = int(game)
                date = player_season_game['date']
                home_team_id = player_season_game['home_team_id']
                home_team_full_name = player_season_game['home_team_full_name']
                home_team_score = player_season_game['home_team_score']
                visitor_team_id = player_season_game['visitor_team_id']
                visitor_team_full_name = player_season_game['visitor_team_full_name']
                visitor_team_score = player_season_game['visitor_team_score']
                qry_insert_game_stats = f"""INSERT INTO PARTIDOS (IDPartido, Fecha, 'IDEquipo local', 'Nombre equipo local', 'Puntos equipo local', 'IDEquipo visitante', 'Nombre equipo visitante', 'Puntos equipo visitante') SELECT '{game_id}', '{date}', '{home_team_id}', '{home_team_full_name}', '{home_team_score}', '{visitor_team_id}', '{visitor_team_full_name}', '{visitor_team_score}' WHERE NOT EXISTS (SELECT 1 FROM PARTIDOS WHERE IDPartido= '{game_id}')"""
                execute_query(self.__connection, qry_insert_game_stats, False)

                player_team_id = season_player_stats[game]['player_team_ID']
                qry_insert_games_played = f"""INSERT INTO PARTIDOS_DISPUTADOS VALUES ('{player_id}', '{game_id}' , '{player_team_id}' , '{season_played_2}')"""
                execute_query(self.__connection, qry_insert_games_played, False)
                    
                mins = season_player_stats[game]['min']
                pts = season_player_stats[game]['pts']
                fg3a = season_player_stats[game]['fg3a']
                fg3m = season_player_stats[game]['fg3m']
                fg2a = season_player_stats[game]['fg2a']
                fg2m = season_player_stats[game]['fg2m']
                fta = season_player_stats[game]['fta']
                ftm = season_player_stats[game]['ftm']
                ast = season_player_stats[game]['ast']
                steal = season_player_stats[game]['stl']
                turnover = season_player_stats[game]['turnover']
                oreb = season_player_stats[game]['oreb']
                dreb = season_player_stats[game]['dreb']
                blk = season_player_stats[game]['blk']
                pf = season_player_stats[game]['pf']
                qry_insert_player_stats = f"""INSERT INTO ESTADISTICAS_PARTIDO_JUGADORES VALUES ('{game_id}', '{player_id}', '{mins}', '{pts}', '{fg3a}', '{fg3m}', '{fg2a}', '{fg2m}', '{fta}', '{ftm}', '{ast}', '{steal}', '{turnover}', '{oreb}', '{dreb}' , '{blk}', '{pf}')"""
                execute_query(self.__connection, qry_insert_player_stats, False) 
                    
        except FileNotFoundError:
            print('Informacion no descargada, revisar uno de los parametros anteriores')


            
               