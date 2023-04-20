# linear regression

# Linear Regression w/ l2 norm (Ridge)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# define general gridsearch for either lasso or ridge model
def lr_gridsearch(func, X_train, X_test, y_train, y_test, features):
    loss_train = []
    loss_test = []
    models = []
    coeffs = []

    # initialize range of lambdas to explore
    lmbds = np.logspace(3, 8, 100)

    for l in lmbds:
        # fit model from func to data
        model = func(alpha = l).fit(X_train, y_train)
        models.append(model)

        # calc and store MSE losses
        loss_train.append(np.mean((y_train - model.predict(X_train))**2))
        loss_test.append(np.mean((y_test - model.predict(X_test))**2))

        # store coefficients
        coeffs.append(model.coef_.flatten())

    # plot train and test MSE
    plt.plot(lmbds, loss_train, label = 'Train')
    plt.plot(lmbds, loss_test, label = 'Test')
    plt.xscale('log')
    plt.xlabel('Lambda')
    plt.ylabel('MSE')
    plt.title('MSE vs Lambda')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          frameon=False, ncol=len(features))
    plt.show()

    # plot coefficients vs lambdas
    #ax = 
    plt.plot(lmbds, coeffs, label = features)
    plt.xscale('log')
    plt.xlabel('Lambda')
    plt.ylabel('Coefficients')
    plt.title('Coefficients vs Lambda')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          frameon=False, ncol=len(features))
    plt.show()


    # find best model, lambda, and MSE based on min MSE test
    best_model = models[np.argmin(loss_test)]
    best_lmbd = lmbds[np.argmin(loss_test)]
    best_MSE = loss_test[np.argmin(loss_test)]

    return [best_model, best_lmbd, best_MSE]

def lr(X, y):
    print('hi')