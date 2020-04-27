import pandas as pd 

predictions = pd.read_csv('modelPredictions.csv')

models = ['XGBoost', 'Logit', 'SVM' , 'Random Forest']


for model in models: 
    subset = predictions[predictions['Model'] = model]

    correct = subset[subset['Correct'] = True]
    incorrect = subset[subset['Correct'] = False]

    for col in subset.columns(): 