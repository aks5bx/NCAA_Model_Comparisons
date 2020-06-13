import pandas as pd 

predictions = pd.read_csv('modelPredictions.csv')

models = ['XGBoost', 'Logit', 'SVM' , 'Random Forest']


for model in models: 
    subset = predictions[predictions['Model'] == model]

    correct = subset[subset['Correct'] == True]
    incorrect = subset[subset['Correct'] == False]

    x = (list(subset.columns)) 

    for col in x: 
        if col == 'Ind' or col == 'Model': 
            continue

        print(model)
        print(col)
        correctAvg = correct[col].mean()
        incorrectAvg = incorrect[col].mean()

        diff = (correctAvg - incorrectAvg) / correctAvg
        print('Correct: ', correctAvg)
        print('Incorrect: ', incorrectAvg)
        print(diff) 
        print('-----------')

    