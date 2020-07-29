#######################################
############# REGRESSION ##############
#######################################

## Importing important libraries
import pandas as pd
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings("ignore")

# technical debt: regressionData = pd.read_csv('feedToModelData.csv') 
regressionData = pd.read_csv('feedToModelData2.csv', index_col = 0)
regressionData = regressionData.dropna()
regressionData = shuffle(regressionData)

## Separating explanatory variables from dependent variable
x = regressionData[regressionData.columns[2:]]
x = x.loc[:, x.columns != 'Team1Win']

## Scaling the data using a standard scaler (scales data using mean and stdev)
standardScalerX = StandardScaler()
x = standardScalerX.fit_transform(x)

## Separating out dependent variable
y = regressionData['Team1Win']

## Train/Test splitting
X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0, test_size=0.2)

## Initiating logit model
logit_model = LogisticRegression()

# Create regularization penalty space
penalty = ['l1', 'l2''elasticnet', 'none']

# Create regularization hyperparameter space
C = np.logspace(0, 4, 10)

# Create hyperparameter options
hyperparameters = dict(C=C, penalty=penalty)

## Optimizing parameters using grid search
clf = GridSearchCV(logit_model, hyperparameters, cv=5, verbose=0)

## Fitting/training model
model = clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# technical debt: print(model.predict_proba(x))

## Report the model score (accuracy)
print('Accuracy :', round(model.score(X_test, y_test), 5) * 100, '%')

## Report the model score (f1)
print('F1 Score :', round(f1_score(y_test, y_pred, average="macro") , 5) * 100, '%')

## Producing proof of concept confusion matrix
cm = confusion_matrix(y_test, model.predict(X_test))

fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(cm)
ax.grid(False)
ax.xaxis.set(ticks=(0, 1), ticklabels=('Predicted 0s', 'Predicted 1s'))
ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual 0s', 'Actual 1s'))
ax.set_ylim(1.5, -0.5)
for i in range(2):
    for j in range(2):
        ax.text(j, i, cm[i, j], ha='center', va='center', color='red')


## Preparing the predictions into a dataframe and writing them to a main predictions (modelPrections) collector 
logitpredictions = pd.DataFrame(X_test)
logitpredictions['Prediction'] = model.predict(X_test)
logitpredictions['Actual'] = y_test.values
logitpredictions['Correct'] = (logitpredictions['Prediction'] == logitpredictions['Actual'])
logitpredictions['Model'] = 'Logit'
 
logitpredictions.to_csv('logitPredictions.csv')

logitpredictions.to_csv('modelPredictions.csv', mode = 'a', header = False)


