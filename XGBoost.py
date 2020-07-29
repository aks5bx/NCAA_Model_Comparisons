## Importing useful libraries
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import random
from tqdm import tqdm

## Read in data, drop nulls, shuffle data
# regressionData = pd.read_csv('feedToModelData.csv') 
regressionData = pd.read_csv('feedToModelData2.csv', index_col = 0) 
regressionData = regressionData.dropna()
regressionData = shuffle(regressionData)

## Isolate explanatory variable data
x = regressionData[regressionData.columns[2:]]
x = x.loc[:, x.columns != 'Team1Win']

## Scale data using standard scaling
standardScalerX = StandardScaler()
x = standardScalerX.fit_transform(x)

## Isolate dependent variable data
y = regressionData['Team1Win']

## Separate out train/test data
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=random.randint(0, 100))

## Use this to find optimal combination manually
#lr_list = [0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 1.5, 2]
#estimators = [20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200]
#features = [2,3,4,5,6,7,8,10]
#depths = [2,3,4,5,6,7,8]

## After the optimization loop runs, these are the optimal parameters
lr_list = [0.25]
estimators = [160]
features = [2]
depths = [8]

## Optimization Loop
best = 0
for learning_rate in tqdm(lr_list):
    for estimator in tqdm(estimators): 
        for feature in features: 
            for depth in depths: 
                gb_clf = GradientBoostingClassifier(n_estimators=estimator, learning_rate=learning_rate, max_features=feature, max_depth=depth, random_state=random.randint(0, 100))
                gb_clf.fit(X_train, y_train)

                if gb_clf.score(X_test, y_test) > best: 
                    best = gb_clf.score(X_test, y_test)

                    print('---------------------------------------------')
                    print('Max Features :', feature)
                    print('Depth :', depth)
                    print('Estimators: ', estimator)
                    print("Learning rate: ", learning_rate)
                    print("Accuracy score (training): {0:.3f}".format(gb_clf.score(X_train, y_train)))
                    print("Accuracy score (validation): {0:.3f}".format(gb_clf.score(X_test, y_test)))

                    predictions = gb_clf.predict(X_test)
                    print(confusion_matrix(y_test, predictions))

                    X_testFinal = X_test


## Generate predictions and related information
xgBoostPredictions = pd.DataFrame(X_testFinal) 
xgBoostPredictions['Prediction'] = predictions
xgBoostPredictions['Actual'] = y_test.values
xgBoostPredictions['Correct'] = (xgBoostPredictions['Prediction'] == xgBoostPredictions['Actual'])
xgBoostPredictions['Model'] = 'XGBoost'

## Write to csv
xgBoostPredictions.to_csv('xgBoostPredictions.csv')
xgBoostPredictions.to_csv('modelPredictions.csv', mode = 'a', header = False)
