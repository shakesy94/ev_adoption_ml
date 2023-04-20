# random_forest.py
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn import tree

def rf_train(X, y):
    # Train initial baseline model
    start_time = time.time()
    model = RandomForestRegressor(random_state = 123).fit(X, y)
    elapsed_time = time.time() - start_time
    print('Initial default model time = ', elapsed_time)


    ### CV Parameters if we have enough compute time

    # parameters = {"max_depth" : [3,4,5,6,7,8,9,10],
    #              "min_samples_split": [10, 20, 30, 40 ],
    #              "min_samples_leaf":[1,2,3,4,5,6,7,8,9,10],
    #              "min_weight_fraction_leaf":[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
    #              "max_features":["auto","log2","sqrt",None],
    #              "max_leaf_nodes":[None,10,20,30,40,50,60,70,80,90]}

    # parameters = {"max_features": [1, 2, 3, 4, 5, 6, 7]}
    parameters = {"max_features": [1, 2]}

    # Set up CV Model
    tuning_model = GridSearchCV(model,
                                param_grid = parameters,
                                scoring='neg_mean_squared_error',
                                cv = 5, 
                                verbose=False)

    # CV
    start_time = time.time()
    tuning_model.fit(X, y)
    elapsed_time = time.time() - start_time
    print('CV model time = ', elapsed_time)

    # Store best parameters
    best_parms = tuning_model.best_params_
    best_parms['random_state'] = 123

    # Retrain Optimal model with best parameters
    start_time = time.time()
    model = RandomForestRegressor(**best_parms).fit(X, y)
    elapsed_time = time.time() - start_time
    print('Optimal model time = ', elapsed_time)

    return model

def feat_importance(model, X_train, y_train, feature_names):
    # Feature importance for the trained model

    # Impurity-based approach
    start_time = time.time()
    importances = model.feature_importances_
    std = np.std([tree.feature_importances_ for tree in model.estimators_], axis=0)
    elapsed_time = time.time() - start_time

    print(f"Elapsed time to compute the importances: {elapsed_time:.3f} seconds")

    # Plot impurity based features
    forest_importances = pd.Series(importances, index = feature_names)

    fig, ax = plt.subplots()
    forest_importances.plot.bar(yerr=std, ax=ax)
    ax.set_title("Feature importances using MDI")
    ax.set_ylabel("Mean decrease in impurity")
    fig.tight_layout()

    # Permutation-based approach
    start_time = time.time()
    result = permutation_importance(
        model, X_train, y_train, n_repeats = 10, random_state = 123, n_jobs=2
    )
    # here we are calulating the feature importance of the train set so that we can compare it with impurity based feature importance 
    # but you can calculate on the test set as well 
    elapsed_time = time.time() - start_time
    print(f"Elapsed time to compute the importances: {elapsed_time:.3f} seconds")

    # Plot permutation-based features
    forest_importances = pd.Series(result.importances_mean, index = feature_names)

    fig, ax = plt.subplots()
    forest_importances.plot.bar(yerr=result.importances_std, ax=ax)
    ax.set_title("Feature importances using permutation on full model")
    ax.set_ylabel("Mean accuracy decrease")
    fig.tight_layout()
    plt.show()