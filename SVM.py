from sklearn import svm

import pandas as pd
regressionData = pd.read_csv('feedToModelData.csv') 
regressionData = regressionData.dropna()

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler 

## from sklearn.datasets.samples_generator import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix

from sklearn import metrics

x = regressionData[regressionData.columns[3:75]]
standardScalerX = StandardScaler()
x = standardScalerX.fit_transform(x)

y = regressionData['Team1Win']

X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0, test_size=0.2)


clf = svm.SVC(kernel='linear', C = 10.0, degree = 3) # Linear Kernel

#Train the model using the training sets
clf.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

SVMPredictions = pd.DataFrame(X_test)
SVMPredictions['Prediction'] = clf.predict(X_test)
SVMPredictions['Actual'] = y_test.values
SVMPredictions['Correct'] = (SVMPredictions['Prediction'] == SVMPredictions['Actual'])
SVMPredictions['Model'] = 'SVM'


SVMPredictions.to_csv('SVMPredictions.csv')

SVMPredictions.to_csv('modelPredictions.csv', mode = 'a', header = False)




'''
import pandas as pd
regressionData = pd.read_csv('feedToModelData.csv') 
regressionData = regressionData.dropna()

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler 

import cvxopt
from sklearn.datasets.samples_generator import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix

x = regressionData[regressionData.columns[3:75]]
standardScalerX = StandardScaler()
x = standardScalerX.fit_transform(x)

y = regressionData['Team1Win']


X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0)

svm = SVM()
svm.fit(X_train, y_train)
'''