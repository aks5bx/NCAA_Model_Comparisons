#######################################
############# REGRESSION ##############
#######################################

import pandas as pd
from sklearn.utils import shuffle

# regressionData = pd.read_csv('feedToModelData.csv') 
regressionData = pd.read_csv('feedToModelData2.csv', index_col = 0)
regressionData = regressionData.dropna()
regressionData = shuffle(regressionData)


import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import warnings
warnings.filterwarnings("ignore")


x = regressionData[regressionData.columns[2:]]
x = x.loc[:, x.columns != 'Team1Win']


standardScalerX = StandardScaler()
x = standardScalerX.fit_transform(x)

y = regressionData['Team1Win']

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




#model = LogisticRegression(solver='liblinear', random_state=0, max_iter = 10000, C = 50.0)
#model.fit(X_train, y_train)

# print(model.predict_proba(x))
print(round(model.score(X_test, y_test), 5) * 100, '%')

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
# plt.show()



logitpredictions = pd.DataFrame(X_test)
logitpredictions['Prediction'] = model.predict(X_test)
logitpredictions['Actual'] = y_test.values
logitpredictions['Correct'] = (logitredictions['Prediction'] == logitredictions['Actual'])
logitpredictions['Model'] = 'Logit'
 
logitpredictions.to_csv('logitPredictions.csv')

logitpredictions.to_csv('modelPredictions.csv', mode = 'a', header = False)


