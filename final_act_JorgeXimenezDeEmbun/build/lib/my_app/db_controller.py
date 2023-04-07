import sqlite3
from sqlite3 import Error
import json

from my_app.controller import Controller

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Conexión a BD SQLite satisfactoriamente.")
        connection.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(f"Error: '{e}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Consulta ejecutada satisfactoriamente.")
    except Error as e:
        print(f"Error: '{e}'")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        print('JUGADORES EXISTENTES')
        column_names = [description[0] for description in cursor.description]
        print(column_names)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Error: '{e}'")


class Dbcontroller:

    def __init__(self):
        self.__bbdd = 'Base_datos_estadisticas_basket.db'

    def launch_db_controller(self):
    
        self.__connection = create_connection(self.__bbdd)

        opcion = -1
        while opcion != 4:
            print("""
                1) Consultar jugadores de la base de datos      
                2) Cargar estadisticas por jugador y temporadas
                3) Cargar informacion partidos por jugador y temporadas  
                4) Salir
                """)

            opcion=input("¿Qué desea hacer?")
    

        if opcion=="1":

            select_players = "SELECT * from JUGADORES"
            players = execute_read_query(self.__connection, select_players) 
            if players:
                for player in players:
                    print(player)


        elif opcion=="2":

            player_name_2 = input('Inserte el nombre del jugador:')
            season_played_2 = input('Inserte la temporada:')
            controller_2 = Controller(player_name_2, season_played_2,0)
            controller_2.downloading_players_info()
            
            try:
                with open(f'my_app/my_app_saved_files/players_requested/{player_name_2}.json', 'r') as player_file:
                    player_info = json.load(player_file)
                player_id = player_info['id']
                player_name = player_info['first name'] + player_info['last name']
                player_position = player_info['position']
                player_height = player_info['height_feet']
                player_weight = player_info['weight_pounds']
                qry_insert_player = 'INSERT INTO JUGADORES VALUES (' + player_id + ',' + player_name + ',' + player_position + ',' + player_height + ',' + player_weight +')'
                execute_query(self.__connection, qry_insert_player)  

                with open(f'my_app/my_app_saved_files/stats_players_requested/{player_name_2}_{season_played_2}.json', 'r') as stats_player_file:
                    season_player_stats = json.load(stats_player_file)
                for k in season_player_stats.keys():
                    game_id = season_player_stats[k]['game_ID']
                    player_team_id = season_player_stats[k]['player_team_ID']
                    qry_insert_games_played = 'INSERT INTO PARTIDOS_DISPUTADOS VALUES (' + player_id + ',' + game_id + ',' + player_team_id + ',' + season_played_2 + ')'
                    execute_query(self.__connection, qry_insert_games_played)
                    
                    mins = season_player_stats[k]['min']
                    pts = season_player_stats[k]['pts']
                    fg3a = season_player_stats[k]['fg3a']
                    fg3m = season_player_stats[k]['fg3m']
                    fg2a = season_player_stats[k]['fg2a']
                    fg2m = season_player_stats[k]['fg2m']
                    fta = season_player_stats[k]['fta']
                    ftm = season_player_stats[k]['ftm']
                    ast = season_player_stats[k]['ast']
                    steal = season_player_stats[k]['steal']
                    turnover = season_player_stats[k]['turnover']
                    oreb = season_player_stats[k]['oreb']
                    dreb = season_player_stats[k]['dreb']
                    blk = season_player_stats[k]['blk']
                    pf = season_player_stats[k]['pf']
                    qry_insert_player_stats = 'INSERT INTO ESTADISTICAS_PARTIDO/JUGADORES VALUES (' + player_id + ',' + mins + ',' + pts + ',' + fg3a + ',' + fg3m + ',' + fg2a + ',' + fg2m + ',' + fta + ',' + ftm + ',' + ast + ',' + steal + ',' + turnover + ',' + oreb + ',' + dreb + ',' + blk + ',' + pf + ',' + game_id + ')'
                    execute_query(self.__connection, qry_insert_player_stats) 
            
            except FileNotFoundError:
                print('Informacion no descargada, revisar uno de los parametros anteriores')


        elif opcion=="3":
 
            player_name_3 = input('Inserte el nombre del jugador:')
            season_played_3 = input('Inserte la temporada:')

            with open(f'my_app/my_app_saved_files/stats_players_requested/{player_name_3}_{season_played_3}.json', 'r') as stats_player_file:
                    season_player_stats = json.load(stats_player_file)
            for game in season_player_stats.keys():
                controller_3 = Controller(player_name_3, season_played_3, game)
                controller_3.downloading_game_info()
                with open(f'my_app/my_app_saved_files/games_info/{player_name_3}_{season_played_3}_{game}.json', 'r') as stats_game_file:
                    player_season_game = json.load(stats_game_file)
                game_id = game
                date = player_season_game['date']
                home_team_id = player_season_game['home_team_id']
                home_team_full_name = player_season_game['home_team_full_name']
                home_team_score = player_season_game['home_team_score']
                visitor_team_id = player_season_game['visitor_team_id']
                visitor_team_full_name = player_season_game['visitor_team_full_name']
                visitor_team_score = player_season_game['visitor_team_score']
                qry_insert_game_stats = 'INSERT INTO PARTIDOS VALUES (' + game_id + ',' + date + ',' + home_team_id + ',' + home_team_full_name+ ',' + home_team_score + ',' + visitor_team_id + ',' + visitor_team_full_name + ',' + visitor_team_score + ')'
                execute_query(self.__connection, qry_insert_game_stats) 


        elif opcion=="4":
            print("Adiós")
            exit()
        else:
            print("Opción no válida")