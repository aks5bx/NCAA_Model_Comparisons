#%% 

## Import useful libraries
from sklearn import svm
from sklearn.utils import shuffle
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler 

from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn import metrics

#regressionData = pd.read_csv('feedToModelData.csv') 
#regressionData = regressionData.dropna()

## Read in data, drop nulls, shuffle the dataframe
regressionData = pd.read_csv('feedToModelData2.csv', index_col = 0) 
regressionData = regressionData.dropna()
regressionData = shuffle(regressionData)

## Extract explanatory data
x = regressionData[regressionData.columns[2:]]
x = x.loc[:, x.columns != 'Team1Win']

## Scale data using standard scaler 
standardScalerX = StandardScaler()
x = standardScalerX.fit_transform(x)

## Extract dependent variable data
y = regressionData['Team1Win']

## Develop training, testing split
X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0, test_size=0.2)

## Create grid search space, conduct grid search, and fit model
param_grid = {'C': [0.1,1, 10, 100], 'gamma': [1,0.1,0.01,0.001],'kernel': ['rbf', 'poly', 'sigmoid']}
clf = GridSearchCV(svm.SVC(),param_grid,refit=True,verbose=2)
clf.fit(X_train,y_train)

## Predict the response for test data
y_pred = clf.predict(X_test)

## Return accuracy 
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

## Save prediction information
SVMPredictions = pd.DataFrame(X_test)
SVMPredictions['Prediction'] = clf.predict(X_test)
SVMPredictions['Actual'] = y_test.values
SVMPredictions['Correct'] = (SVMPredictions['Prediction'] == SVMPredictions['Actual'])
SVMPredictions['Model'] = 'SVM' 

## Write to csv
SVMPredictions.to_csv('SVMPredictions.csv')
SVMPredictions.to_csv('modelPredictions.csv', mode = 'a', header = False)

# %%
