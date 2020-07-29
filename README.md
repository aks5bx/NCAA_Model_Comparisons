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

#### Legacy Files 
- Files pertaining to an "NCAA Algorithm" are legacy files from a previous attempt at an NCAA Prediction Algorithm using the same data 
- There are also various other legacy files from previous data sources and tests run during the creation of this project

## Findings
There are a few particular coefficients that seem to exhibit the same difference between cases of correct predictions and incorrect predictions. The difference in scaled value for each coefficient, for each model is shown below, highlighting the difference between what the coefficient value was in correct predictions vs incorrect predictions.

#### Logit 
![alt text](https://github.com/aks5bx/NCAA_Model_Comparisons/blob/Develop/LogitCoefficients.png?raw=true)

#### SVM 
![alt text](https://github.com/aks5bx/NCAA_Model_Comparisons/blob/Develop/SVMCoefficients.png?raw=true)

#### Random Forest 
![alt text](https://github.com/aks5bx/NCAA_Model_Comparisons/blob/Develop/randomForestCoefficients.png?raw=true)

#### XGBoost 
![alt text](https://github.com/aks5bx/NCAA_Model_Comparisons/blob/Develop/XGBoostCoefficients.png?raw=true)

#### Coefficients with Strictly Higher Values when Prediction is Correct 
SOS (Strength of Schedule for Team 1), SOS2 (Strength of Schedule for Team 2)

This seems to make logical sense. As teams have stronger strength of schedules during the regular season, they are "tested" teams. As a result, their play may be less eratic in the NCAA Tournament and therefore easier to predict. As a result, higher strength of schedules may be correlated with correct predictions. 


#### Coefficients with Strictly Higher Values when Prediction is InCorrect 
ST/Pos2 (Steals per possession for Team 2), BL%2 (Block % for Team 2). 

Note that these are both defensive metrics; and, they also may follow logically. As teams have better defenses, their performance may likely depend more on the quality of the offense they face. As a result, defensive minded teams may be more susceptible to random spikes in opponent offensive production and may be more erratic in the NCAA Tournament. As a result, stronger defensive metrics may be correlated with incorrect predictions. 

## Notes and Limitations 

This project serves primarily as a proof of concept. As in, this method of determining which factors make NCAA Basketball games harder to predict can be replicated in order to designate future games that may be particularly hard to predict. This designation can be used for betting purposes, for media promotion, or general fan knowledge. 

This project is severely limited because the original four models used as data sources are not of professional grade accuracy. Instead, they all have accuracy scores around 70%. To reiterate, the goal of this project was not to create the best model; instead it was to try to discern what factors made a game hard to predict. Replicating this project with better, more accurate models would likely result in more accurate results. 

Another limitation to note is that in order to avoid multicollinearity, some explanatory variables were removed (those with high VIFs). As such, these variables were not candidates to be identified as causes of hard-to-predict games. 

