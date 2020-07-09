import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import warnings
warnings.filterwarnings("ignore")

predictions = pd.read_csv('modelPredictions.csv', header = None, index_col = 0)

coefficients =  ['ST/Pos', 'ST/Pos2', 'Margin2', 'Margin', 'Last 102', 'TS%M2',
                       'Last 10', 'FG%M2', 'TS%M', 'BL%2', 'FG%M', 'BL%', 'CGWin%2', 'CGWin%',
                       'Ind', 'SOS2', 'SOS', 'TOM2', 'TOM', 'Prediction', 'Actual', 'Correct', 'Model']

predictions.columns = coefficients

predictions['Correct'] = predictions['Correct'].astype('int')
predictions = predictions.drop(['Prediction', 'Actual'], axis=1)
predictions = predictions[predictions.Model == 'SVM']

x = predictions[predictions.columns[:-2]]


y = predictions['Correct']

X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0, test_size=0.2)



logit_model = LogisticRegression()

# Create regularization penalty space
penalty = ['l1', 'l2''elasticnet', 'none']

# Create regularization hyperparameter space
C = np.logspace(0, 4, 10)

# Create hyperparameter options
hyperparameters = dict(C=C, penalty=penalty)

clf = GridSearchCV(logit_model, hyperparameters, cv=5, verbose=0)

model = clf.fit(X_train, y_train)

print(round(model.score(X_test, y_test), 5) * 100, '%')

model.best_estimator_.coef_



