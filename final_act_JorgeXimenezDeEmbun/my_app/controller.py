import sqlite3
from sqlite3 import Error
from my_app.db_controller import Dbcontroller
from my_app.ml_controller import Mlcontroller

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print('Conexión a BD SQLite satisfactoriamente')
        connection.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(f"Error: '{e}'")

    return connection

class Controller:

    def __init__(self):
        self.__bbdd = 'Base_datos_estadisticas_basket.db'

    def launch_controller(self):
        self.__connection = create_connection(self.__bbdd)
        db_controller = Dbcontroller(self.__connection)
        ml_controller = Mlcontroller(self.__connection)

        option = -1
        while option != 4:
            print("""
                1) Consultar jugadores existentes en base de datos 
                2) Cargar estadisticas de todos los partidos de 
                   una temporada segun el jugador solicitado
                3) Predecir segun estadisticas de un jugador en un
                   partido, si su equipo debería haber ganado y por cuanto
                4) Salir
                """)

            option=input('¿Qué desea hacer?: ')

            if option == '1':
                players = ml_controller.show_players_in_database()
                print(players)

            elif option == '2':
                db_controller.add_player_stats_in_db()

            elif option == '3':
                players = ml_controller.show_players_in_database()
                print(players)
                class_model, reg_model = ml_controller.trainning_model()
                player_stats = [
                                float(input('Minutos jugados: ')),
                                int(input('Puntos: ')),
                                int(input('Asistencias: ')),
                                int(input('Robos: ')),
                                int(input('Perdidas: ')),
                                int(input('Tapones: ')),
                                int(input('Faltas: ')),
                                int(input('Rebotes: '))
                                ]
                
                result_prediction, points_prediction = ml_controller.prediction(class_model, reg_model, player_stats)
                print(f'El jugador gana(0) o pierde(1) el partido: {result_prediction}')
                print(f'El equipo del jugador gana o pierde por: {int(points_prediction)} puntos')

            elif option=='4':
                self.__connection.close()
                print('Adiós')
                exit()
            else:
                print('Opción no válida')