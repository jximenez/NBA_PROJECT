import sqlite3
from sqlite3 import Error
import json
from time import sleep
from random import randint

from my_app.controller import Controller

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print('Conexión a BD SQLite satisfactoriamente')
        connection.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(f"Error: '{e}'")

    return connection

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

    def __init__(self):
        self.__bbdd = 'Base_datos_estadisticas_basket.db'

    def launch_db_controller(self):
    
        self.__connection = create_connection(self.__bbdd)

        option = -1
        while option != 6:
            print("""
                1) Consultar fichas de jugadores    
                2) Cargar estadisticas de todos los partidos de 
                   una temporada segun el jugador solicitado
                3) Cargar medias estadisticas de un jugador en las 
                   temporadas que se deseen
                4) Consultar estadisticas medias de jugador para ver 
                   su grafico de evolucion en las temporadas deseadas
                5) Consultar estadisticas concretas de un jugador en 
                   partidos ganados o perdidos de cualquier temporada
                6) Salir
                """)

            option=input('¿Qué desea hacer?: ')
    

            if option=='1':

                select_players = "SELECT * from JUGADORES"
                players = execute_read_query(self.__connection, select_players) 
                if players:
                    for player in players:
                        print(player)
                else: print('Ningun jugador en la base de datos')

            elif option=='2':

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


            elif option=='3':
 
                player_name_3 = str(input('Inserte el nombre y 1er apellido del jugador: '))
                seasons_list_3 = []
                seasons_range = int(input(
                    """Inserte el numero de temporadas de los que quiere 
                    descargar las medias del jugador solicitado: 
                    """))
                for i in range(seasons_range):
                    season_played_3 = int(input('Inserte una de las temporadas: '))
                    seasons_list_3.append(season_played_3)

                try:
                    controller_3 = Controller(player_name_3, seasons_list_3, 0)
                    controller_3.downloading_average_season_player_stats()

                    with open(f'my_app/my_app_saved_files/players_requested/{player_name_3}.json', 'r') as player_file:
                        player_info = json.load(player_file)
                    player_id = player_info['id']
                    player_name = player_info['first_name'] + ' ' + player_info['last_name']
                    player_position = player_info['position']
                    player_height = player_info['height_feet']
                    player_weight = player_info['weight_pounds']
                    qry_insert_player = f"""INSERT INTO JUGADORES (IDJugador, Nombre, Posicion,Altura,Peso) SELECT '{player_id}' , '{player_name}' , '{player_position}' , '{player_height}' , '{player_weight}' WHERE NOT EXISTS (SELECT 1 FROM JUGADORES WHERE IDJugador= '{player_id}')"""
                    execute_query(self.__connection, qry_insert_player, True)

                    for season in seasons_list_3:
                        with open(f'my_app/my_app_saved_files/average_season_stats/{player_name_3}_{season}_AverageStats.json', 'r') as average_stats_file:
                            average_season_stats = json.load(average_stats_file)
                        season_played = average_season_stats['season']
                        games_played = average_season_stats['games_played']
                        mins = average_season_stats['min']
                        pts = average_season_stats['pts']
                        fg3a = average_season_stats['fg3a']
                        fg3m = average_season_stats['fg3m']
                        fg2a = average_season_stats['fg2a']
                        fg2m = average_season_stats['fg2m']
                        fta = average_season_stats['fta']
                        ftm = average_season_stats['ftm']
                        ast = average_season_stats['ast']
                        steal = average_season_stats['stl']
                        turnover = average_season_stats['turnover']
                        oreb = average_season_stats['oreb']
                        dreb = average_season_stats['dreb']
                        blk = average_season_stats['blk']
                        pf = average_season_stats['pf']
                        qry_insert_average_player_stats = f"""INSERT INTO MEDIAS_ESTADISTICAS_TEMPORADA_JUGADORES VALUES ('{player_id}', '{season_played}', '{games_played}', '{mins}', '{pts}', '{fg3a}', '{fg3m}', '{fg2a}', '{fg2m}', '{fta}', '{ftm}', '{ast}', '{steal}', '{turnover}', '{oreb}', '{dreb}' , '{blk}', '{pf}')"""
                        execute_query(self.__connection, qry_insert_average_player_stats, False)

                except FileNotFoundError:
                    print('Informacion no descargada, revisar uno de los parametros anteriores')


            elif option=='4':
                player_name_4 = str(input('Inserte el nombre y 1er apellido del jugador (1era en Mayuscula): '))
                seasons_list_4 = []
                select_average_player_stats = f"""SELECT * from MEDIAS_ESTADISTICAS_TEMPORADA_JUGADORES METJ INNER JOIN JUGADORES J ON J.IDJugador = METJ.IDJugador WHERE Nombre = '{player_name_4}' """
                average_stats = execute_read_query(self.__connection, select_average_player_stats) 
    
                if average_stats:
                    for season_stats in average_stats:
                        print(season_stats)
                        seasons_list_4.append(season_stats[1])    
                    download_plot = input('¿Desea descargar alguna grafica de evolucion? (si/no): ')
                    if download_plot == 'si':
                        controller_4 = Controller(player_name_4, seasons_list_4, 0)
                        print(""" Graficas disponibles:
                        1) Grafica partidos jugados 
                        2) Grafica minutos disputados
                        3) Grafica puntos
                        4) Grafica asistencias
                        5) Grafica robos                            
                        """)
                        stats_type = input("¿Qué desea hacer?: ") 

                        if stats_type == '1':
                            controller_4.drawing_average_plot(stats_type)
                        if stats_type == '2':
                            controller_4.drawing_average_plot(stats_type)
                        if stats_type == '3':
                            controller_4.drawing_average_plot(stats_type)
                        if stats_type == '4':
                            controller_4.drawing_average_plot(stats_type)
                        if stats_type == '5':
                            controller_4.drawing_average_plot(stats_type)

                    else: pass
                else: print('No hay estadisticas medias del jugador requerido, ir primero a la opcion 3 del menu para descargarlas')


            elif option=='5':
                player_name_5 = str(input('Inserte el nombre y 1er apellido del jugador (1era en Mayuscula): '))
                season_played_5 = int(input('Inserte la temporada a consultar: '))
                game_win_or_lose = str(input('¿Desea consultar los partidos ganados o perdidos? (G/P): '))
                print("""
                ** Estadisticas a consultar en dichos partidos **
                Minutos - Minutos jugados
                Puntos - Puntos conseguidos
                Asistencias - Asistencias por partido
                Robos - Robos por partido
                Perdidas - Perdidas por partido
                """)
                request_stats = input('Escriba solo una de las estadisticas a consultar (ej; Asistencias): ')
                if game_win_or_lose == 'G':
                    select_requested_player_stats = f"""
                    CREATE VIEW IF NOT EXISTS EQUIPOS_GANADORES_{season_played_5} AS 
                    SELECT "IDEquipo local" AS "IDEquipo ganador", P.IDPartido AS IDPartido
                    FROM PARTIDOS P 
                    INNER JOIN PARTIDOS_DISPUTADOS PD ON PD.IDPartido = P.IDPartido
                    WHERE ("Puntos equipo local" > "Puntos equipo visitante") AND PD.Temporada='{season_played_5}' 

                    UNION ALL

                    SELECT "IDEquipo visitante" AS "IDEquipo ganador", P.IDPartido AS IDPartido
                    FROM PARTIDOS P 
                    INNER JOIN PARTIDOS_DISPUTADOS PD ON PD.IDPartido = P.IDPartido
                    INNER JOIN JUGADORES J ON J.IDJugador = PD.IDJugador
                    WHERE ("Puntos equipo local" < "Puntos equipo visitante") AND PD.Temporada='{season_played_5}';
                    """
                    requested_stats = execute_query(self.__connection, select_requested_player_stats, False)
               
                    select_requested_player_stats = f"""
                    SELECT J.Nombre, EPJ.'{request_stats}', "IDEquipo jugador", PD.Temporada, P.IDPartido, P.Fecha, "IDEquipo local", "Nombre equipo local", "Puntos equipo local", "IDEquipo visitante", "Nombre equipo visitante", "Puntos equipo visitante"
                    FROM ESTADISTICAS_PARTIDO_JUGADORES EPJ 
                    INNER JOIN PARTIDOS P ON P.IDPartido = EPJ.IDPartido 
                    INNER JOIN PARTIDOS_DISPUTADOS PD ON PD.IDPartido = P.IDPartido 
                    INNER JOIN JUGADORES J ON J.IDJugador = PD.IDJugador 
                    WHERE J.Nombre='{player_name_5}' AND PD.Temporada='{season_played_5}'
                    AND EPJ.IDPartido IN (SELECT IDPartido FROM EQUIPOS_GANADORES_{season_played_5} WHERE "IDEquipo ganador" IN (SELECT "IDEquipo jugador" FROM PARTIDOS_DISPUTADOS PD INNER JOIN JUGADORES J ON J.IDJugador=PD.IDJugador WHERE J.Nombre='{player_name_5}' AND PD.Temporada='{season_played_5}'))
                    """
                    requested_stats = execute_read_query(self.__connection, select_requested_player_stats)
                    if requested_stats:
                        for requested_stat in requested_stats:
                            print(requested_stat)
                    else: print('No existen datos con los valores solicitados')

                if game_win_or_lose == 'P':
                    select_requested_player_stats = f"""
                    CREATE VIEW IF NOT EXISTS EQUIPOS_PERDEDORES_{season_played_5} AS 
                    SELECT "IDEquipo local" AS "IDEquipo perdedor", P.IDPartido AS IDPartido
                    FROM PARTIDOS P 
                    INNER JOIN PARTIDOS_DISPUTADOS PD ON PD.IDPartido = P.IDPartido
                    WHERE ("Puntos equipo local" < "Puntos equipo visitante") AND PD.Temporada='{season_played_5}' 

                    UNION ALL

                    SELECT "IDEquipo visitante" AS "IDEquipo perdedor", P.IDPartido AS IDPartido
                    FROM PARTIDOS P 
                    INNER JOIN PARTIDOS_DISPUTADOS PD ON PD.IDPartido = P.IDPartido
                    WHERE ("Puntos equipo local" > "Puntos equipo visitante") AND PD.Temporada='{season_played_5}';
                    """
                    requested_stats = execute_query(self.__connection, select_requested_player_stats, False)
                    
                    select_requested_player_stats = f"""
                    SELECT J.Nombre, EPJ.'{request_stats}', "IDEquipo jugador", PD.Temporada, P.IDPartido, P.Fecha, "IDEquipo local", "Nombre equipo local", "Puntos equipo local", "IDEquipo visitante", "Nombre equipo visitante", "Puntos equipo visitante"
                    FROM ESTADISTICAS_PARTIDO_JUGADORES EPJ 
                    INNER JOIN PARTIDOS P ON P.IDPartido = EPJ.IDPartido 
                    INNER JOIN PARTIDOS_DISPUTADOS PD ON PD.IDPartido = P.IDPartido 
                    INNER JOIN JUGADORES J ON J.IDJugador = PD.IDJugador 
                    WHERE J.Nombre='{player_name_5}' AND PD.Temporada='{season_played_5}'
                    AND EPJ.IDPartido IN (SELECT IDPartido FROM EQUIPOS_PERDEDORES_{season_played_5} WHERE "IDEquipo perdedor" IN (SELECT "IDEquipo jugador" FROM PARTIDOS_DISPUTADOS PD INNER JOIN JUGADORES J ON J.IDJugador=PD.IDJugador WHERE J.Nombre='{player_name_5}' AND PD.Temporada='{season_played_5}'))
                    """
                    requested_stats = execute_read_query(self.__connection, select_requested_player_stats)
                    if requested_stats:
                        for requested_stat in requested_stats:
                            print(requested_stat)
                    else: print('No existen datos con los valores solicitados')

            elif option=='6':
                print('Adiós')
                exit()
            else:
                print('Opción no válida')
