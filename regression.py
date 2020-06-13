#######################################
############# REGRESSION ##############
#######################################

import pandas as pd
regressionData = pd.read_csv('feedToModelData.csv') 

regressionData = regressionData.dropna()

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import train_test_split

x = regressionData[regressionData.columns[3:75]]

standardScalerX = StandardScaler()
x = standardScalerX.fit_transform(x)

y = regressionData['Team1Win']

X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0, test_size=0.2)

model = LogisticRegression(solver='liblinear', random_state=0, max_iter = 10000, C = 50.0)
model.fit(X_train, y_train)

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



logitredictions = pd.DataFrame(X_test)
logitredictions['Prediction'] = model.predict(X_test)
logitredictions['Actual'] = y_test.values
logitredictions['Correct'] = (logitredictions['Prediction'] == logitredictions['Actual'])
logitredictions['Model'] = 'Logit'
 
logitredictions.to_csv('logitPredictions.csv')

logitredictions.to_csv('modelPredictions.csv', mode = 'a', header = False)


