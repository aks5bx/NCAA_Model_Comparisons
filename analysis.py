## Import useful libraries
import pandas as pd 
import matplotlib.pyplot as plt

## Read in prediction data
predictions = pd.read_csv('modelPredictions.csv', header = None, index_col = 0)

## Define prediction dataframe columns, which are the regression coefficient
coefficients =  ['ST/Pos', 'ST/Pos2', 'Margin2', 'Margin', 'Last 102', 'TS%M2',
                       'Last 10', 'FG%M2', 'TS%M', 'BL%2', 'FG%M', 'BL%', 'CGWin%2', 'CGWin%',
                       'Ind', 'SOS2', 'SOS', 'TOM2', 'TOM', 'Prediction', 'Actual', 'Correct', 'Model']

predictions.columns = coefficients
    
## Define the four models to iterate through
models = ['XGBoost', 'Logit', 'SVM' , 'Random Forest']

## Set up data structures 
XGBoostList = []
LogitList = []
SVMList = []
RFList = []

XGBoostListCorrect = []
XGBoostListIncorrect = []
LogitListCorrect = []
LogitListIncorrect = []
SVMListCorrect = []
SVMListIncorrect = []
RFListCorrect = []
RFListIncorrect = []

## Loop through each model
for model in models: 
    ## Isolate data for the model at hand
    subset = predictions[predictions['Model'] == model]

    correct = subset[subset['Correct'] == True]
    incorrect = subset[subset['Correct'] == False]

    x = (list(subset.columns)) 

    ## Iterate through each coefficient 
    for col in x: 
        if col == 'Ind' or col == 'Model' or col == 'Correct': 
            continue
        
        ## Compare the coefficients for a correct vs incorrect prediction
        correctAvg = correct[col].mean()
        incorrectAvg = incorrect[col].mean()

        diff = (correctAvg - incorrectAvg) / correctAvg
        
        
        if model == 'XGBoost':
            XGBoostList.append(diff)
            
            XGBoostListCorrect.append(correctAvg)
            XGBoostListIncorrect.append(incorrectAvg)
            
            
        elif model == 'Logit':
            LogitList.append(diff) 
            
            LogitListCorrect.append(correctAvg)
            LogitListIncorrect.append(incorrectAvg)
            
            
        elif model == 'SVM':
            SVMList.append(diff)
            
            SVMListCorrect.append(correctAvg)
            SVMListIncorrect.append(incorrectAvg)
            
            
        elif model == 'Random Forest':
            RFList.append(diff)
            
            RFListCorrect.append(correctAvg)
            RFListIncorrect.append(incorrectAvg)
        

## Remove unimportant coefficients
coefficients.remove('Ind')
coefficients.remove('Model')
coefficients.remove('Correct')

## XGBoost
XGBoostResults = pd.DataFrame(
    {
     'coefficients' : coefficients, 
     'CorrectCoefficientValues' : XGBoostListCorrect, 
     'IncorrectCoefficientValues' : XGBoostListIncorrect
     }
    )

XGBoostResults.set_index('coefficients', inplace=True)

XGBoostResults.plot.bar()

## Logit
LogitResults = pd.DataFrame(
    {
     'coefficients' : coefficients, 
     'CorrectCoefficientValues' : LogitListCorrect, 
     'IncorrectCoefficientValues' : LogitListIncorrect
     }
    )

LogitResults.set_index('coefficients', inplace=True)

LogitResults.plot.bar()


## SVM 
SVMResults = pd.DataFrame(
    {
     'coefficients' : coefficients, 
     'CorrectCoefficientValues' : SVMListCorrect, 
     'IncorrectCoefficientValues' : SVMListIncorrect
     }
    )

SVMResults.set_index('coefficients', inplace=True)

SVMResults.plot.bar()

## Random Forest
RFResults = pd.DataFrame(
    {
     'coefficients' : coefficients, 
     'CorrectCoefficientValues' : RFListCorrect, 
     'IncorrectCoefficientValues' : RFListIncorrect
     }
    )

RFResults.set_index('coefficients', inplace=True)

RFResults.plot.bar()

plt.show()

###############
### Results ###
###############

# ST/Pos - inconclusive
# ST/Pos2 - higher value when incorrect
# Margin2 - inconclusive
# Margin - inconclusive
# Last10_2 - inconclusive
# TS%M2 - inconclusive
# Last 10 - inconclusive
# FG%M 2 - inconclusive
# TS%M - inconclusive
# BL%2 - higher value when incorrect 
# FG%M - inconclusive
# BL% - inconclusive
# CGWin%2 - inconclusive
# CGWin% - inconclusive
# SOS2 - higher when correct
# SOS - higher when correct 
# TOM2 - inconclusive
# TOM - slightly higher when incorrect











