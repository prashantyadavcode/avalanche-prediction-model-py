from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
import pandas as pd
import pickle
#import matplotlib.pyplot as plt
import numpy as np


if __name__=='__main__':
    # load data
    df = pickle.load( open( 'pkl/aspen_d2_imputemean_alldays.p', 'rb'))
    df.drop('N_AVY', axis=1, inplace=True)
    # fill na with zero in case any not imputed
    df.fillna(0, inplace=True)

    ''' case : slab or wet '''
    cases = [['SLAB','WET'], ['WET','SLAB']]

    ''' run case   '''
    case = cases[1] # chose case here, 0 or 1
    data_df = df.copy() # copy to read all columns after dropping

    # drop other binary and probability column
    c_drop = [c for c in list(df.columns) if case[1] in c]
    data_df.drop(c_drop, axis=1, inplace=True)

    # train test split in time
    splitdate = pd.to_datetime('2016-06-01')
    train_df = data_df[data_df.index <= splitdate]
    test_df = data_df[data_df.index > splitdate]

    # oversample train data
    train_shuffle = train_df

    ''' select features and target X,y '''
    # train set
    X_train = train_shuffle.copy()
    y_train = X_train.pop(case[0])
    # test set
    X_test = test_df.copy()
    y_test = X_test.pop(case[0])
    # datetime for plot
    test_datetime = pd.to_datetime(X_test.index)


    # train model
    param_grid = {
        'n_estimators': [500, 600, 700],
        'criterion': ['gini'],
        'max_features': ['log2'],
        'min_samples_split': [8, 9, 10, 11, 12],
        'min_samples_leaf': [7, 8, 9, 10, 11],
        'oob_score': [True],
        'n_jobs': [-1],
        'verbose': [1]
        }

    est = RandomForestClassifier()

    grid = GridSearchCV(est, param_grid, scoring='recall')
    grid.fit(X_train, y_train)

    y_hat = grid.predict(X_test)

    print('case: {}'.format(case[0]))

    score_a = accuracy_score(y_test, y_hat)
    print('test accuracy = {:0.3f}'.format(score_a))

    score_r = recall_score(y_test, y_hat)
    print('test recall = {:0.3f}'.format(score_r))

    print(grid.best_params_)

    best_est = grid.best_estimator_

    pickle.dump(best_est, open("best-ests/best_est_rfc_{}.p".format(case[0]), "wb"))
