import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import random
from tqdm import tqdm


regressionData = pd.read_csv('feedToModelData.csv') 
regressionData = regressionData.dropna()
regressionData = shuffle(regressionData)

x = regressionData[regressionData.columns[3:75]]

standardScalerX = StandardScaler()

x = standardScalerX.fit_transform(x)

y = regressionData['Team1Win']


X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=random.randint(0, 100))

clf=RandomForestClassifier(n_estimators=200)

#Train the model using the training sets y_pred=clf.predict(X_test)
clf.fit(X_train,y_train)

y_pred=clf.predict(X_test)

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

randomForestPredictions = pd.DataFrame(X_test)
randomForestPredictions['Prediction'] = clf.predict(X_test)
randomForestPredictions['Actual'] = y_test.values
randomForestPredictions['Correct'] = (randomForestPredictions['Prediction'] == randomForestPredictions['Actual'])
randomForestPredictions['Model'] = 'Random Forest' 

randomForestPredictions.to_csv('randomForestPredictions.csv')

randomForestPredictions.to_csv('modelPredictions.csv', mode = 'a', header = False)

