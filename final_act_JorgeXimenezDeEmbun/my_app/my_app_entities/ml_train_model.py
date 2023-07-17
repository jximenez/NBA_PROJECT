import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

class MlTrainModel:
    def __init__(self, df_data):
        self.__df_data = df_data
    
    def __encode_features(self, df, features):
        '''
        Funcion para codificar columna result para nuestro modelo
        '''

        for feature in features:
            le = preprocessing.LabelEncoder()
            le = le.fit(df[feature])
            df[feature] = le.transform(df[feature])


    def train_model(self):
        features = ['Resultado']
        self.__encode_features(self.__df_data, features)

        # Classifier KNeighbors and DecisionTreeClassifier
        feature_cols = ['Minutos', 'Puntos', 'Asistencias', 'Robos', 'Perdidas', 'Tapones', 'Faltas', 'Rebotes']
        X = self.__df_data[feature_cols]
        y_class = self.__df_data['Resultado']

        k_range = list(range(1, 31))
        weight_options = ['uniform', 'distance']
        param_grid_knn = dict(n_neighbors=k_range, weights=weight_options)
        knn = KNeighborsClassifier()
        grid_knn = GridSearchCV(knn, param_grid_knn, cv=10, scoring='accuracy')
        grid_knn.fit(X, y_class)

        depth_range = list(range(4, 17, 2))
        random_range = list(range(2, 43, 8))
        param_grid_dct = dict(max_depth=depth_range, random_state=random_range)
        dtc = DecisionTreeClassifier()
        grid_dtc = GridSearchCV(dtc, param_grid_dct, cv=10, scoring='accuracy')
        grid_dtc.fit(X, y_class)

        if grid_dtc.best_score_ > grid_knn.best_score_:
            best_classifier_model = grid_dtc.best_estimator_
        else: best_classifier_model = grid_knn.best_estimator_

        # Regression LinearRegression and DecisionTreeClassifier
        feature_cols = ['Minutos', 'Puntos', 'Asistencias', 'Robos', 'Perdidas', 'Tapones', 'Faltas', 'Rebotes']
        X = self.__df_data[feature_cols]
        y_reg = self.__df_data['Puntos diferencia']

        n_jobs_range = list(range(4, 17, 2))
        param_grid_linreg = dict(n_jobs=n_jobs_range)
        linreg = LinearRegression()
        grid_linreg = GridSearchCV(linreg, param_grid_linreg, cv=10, scoring='neg_root_mean_squared_error')
        grid_linreg.fit(X, y_reg)

        depth_range = list(range(4, 17, 2))
        random_range = list(range(2, 43, 8))
        param_grid_dtr = dict(max_depth=depth_range, random_state=random_range)
        dtr = DecisionTreeRegressor()
        grid_dtr = GridSearchCV(dtr, param_grid_dtr, cv=10, scoring='neg_root_mean_squared_error')
        grid_dtr.fit(X, y_reg)

        if grid_dtr.best_score_ > grid_linreg.best_score_:
            best_regression_model = grid_dtr.best_estimator_
        else: best_regression_model = grid_linreg.best_estimator_

        return(best_classifier_model, best_regression_model)