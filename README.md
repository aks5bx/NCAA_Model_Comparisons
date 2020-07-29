# NCAA_Model_Comparisons

## Project Overview
This project seeks to generate simple models that predict the Win/Loss of an NCAA March Madness game. The models in consideration include SVM, xgBoost, Logistic Regression, and Random Forest. 

The overall goal is to analyze these four models and determine which types of games are particularly difficult to predict with these types of Machine Learning models. The goal of this project is not to do the best job at predicting March Madness games - instead the goal is to understand what game characteristics present the largest challenge to taming the uncertainty of March Madness. 

## Technology Used 
This project primarily uses python, with a strong reliance on the pandas and scikit-learn packages. 

## File Directory
#### Starting Point Data Sets 
- (Year).csv : These csvs contain basic data for NCAAM Tournament teams in a given year, primarily taken from https://www.teamrankings.com/ncb/stats/
- matchups.csv : This csv contains the matchups (which teams played which teams) of various NCAAM tournaments

#### Data Engineering/Prep
- webscrape.py : Scrapes https://www.teamrankings.com/ncb/stats/ in order to get additionalal aggregate NCAAM Team Statistics for each year from 2008 - 2019, uses Year.csv files as a baseline, but adds additional aggregate statistics; ultimately produces collectorDF.csv
- collectorDF.csv : intermediate data step
- fullData.csv : takes collectorDF.csv and adds a few more data fields (manually added) to end with a more complete dataset
- dataPrep.py : takes fullData.csv and matchups.csv and creates a single row with both teams & their corresponding statistics, ultimately creating regressionData.csv 
- regressionUseData.csv : cleans regressionData.csv 
- shuffleData.py : shuffles/randomizes the data order to remove spurious patterns, produces feedToModelData.csv
- feedToModelData2.csv : final csv that can be fed into a Machine Learning model 

#### Model Generation
- regression.py : multivariate regression, includes basic feature engineering using a Standard Scaler
- randomForest.py : random forest method, includes basic feature engineering using a Standard Scaler
- SVM.py : support vector machine algorithm with linear kernel, includes basic feature engineering using a Standard Scaler 
- XGBoost.py: extreme gradient boosting algorithm, includes iterative parameter tuning and basic feature engineering using a Standard Scaler 

#### Analysis 
- analysis.py: Looks into the average value of a field, for each algorithm, when the prediction was correct vs incorrect

## Findings
There are a few particular coefficients that seem to exhibit the same difference between cases of correct predictions and incorrect predictions. The difference in scaled value for each coefficient, for each model is shown below, highlighting the difference between what the coefficient value was in correct predictions vs incorrect predictions.

#### Logit 
![alt text](https://github.com/aks5bx/NCAA_Model_Comparisons/blob/Develop/LogitCoefficients.png =10x)




