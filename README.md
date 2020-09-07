# NCAA_Model_Comparisons

## Project Overview
This project seeks to generate simple models that predict the Win/Loss of an NCAA March Madness game. The models in consideration include SVM, xgBoost, Logistic Regression, and Random Forest. 

The overall goal is to analyze these four models and determine which types of games are particularly difficult to predict with these types of Machine Learning models. The goal of this project is not to do the best job at predicting March Madness games - instead the goal is to understand what game characteristics present the largest challenge to taming the uncertainty of March Madness. 

From start to finish, this project includes: 
- Webscraping 
- Data Engineering
- Feature Engineering/Scaling 
- Machine Learning 
- Analysis/Interpretation

## Process
The process of executing this project is as follows
1. Collect Data (webscraping)
2. Clean Data, Conduct Feature Engineering
3. Build and Execute Models 
*The four models used are Random Forest, SVM, Logit, and XGBoost. These models were used in order to create a wide variety in approaches. The models give us a set of coefficients along with a game prediction for each game. We have the data to also determine whether the game prediction was correct or incorrect.*
4. Analyze model coefficients 
*For each model, the data was split into data from correct game predictions and data from incorrect game predictions. Then, for each group, the average coefficient was recorded. For example, in cases of incorrect predictions, the Block %s for each team were recorded. Then, for cases of correct predictions, the Block %s were recorded for each team. This allows us to compare the Block %s in cases where the prediction was incorrect vs correct. As is discussed later in this write up, one example is that when game predictions are correct, Strength of Schedules tend to be higher for both teams (compared to Strength of Schedules from incorrect game predictions). As a result, we can posit that when a game features two teams with strong strengths of schedules, that game may be easier to predict.* 
5. Report Findings

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

## Data Overview
The data is formated with the following fields 
- Game Statistics for Team 1 (SOS, FG%, etc)
- Game Statistics for Team 2 (SOS2, FG%2, etc)
- Binary field for "Did Team 1 Win"

Here are some of the metrics used:
- ST/Pos: Steals per possesion
- Margin: Turnover margin 
- Last 10: wins in the last 10 games 
- TS%M: True Shooting Margin 
- FG%M: Field Goal % Margin
- BL%: Block percentage 
- CGWin%: Close Game Win %
- All metrics available for both teams


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


#### Two Sample T Test Confirmation 
In order to confirm that the trends identified with the help of the bar charts above are statistically significant, we employ a two sample t-test. It is worth noting that a two sample t test assumes two independent samples. In this case, the samples are not fully independent, but there is no data overlap between the two samples given their mutual exclusivity (one sample is where the prediction was correct while the other is where the prediction was not correct). As such, we consider the samples independent as far as the requirements for the t-test are concerned. Below is a table with all of the coefficients that have statistically significant (p value less than 0.1) differences when the prediction is correct vs incorrect. (2 is denoted for team 2 coefficient, coefficients for team 1 are left unmarked). 

| Model  | Coefficient | P-Value |
| ------------- | ------------- | ------------- |
| XGBoost  | Last 10 (2)  | 0.05760942341856636  |
| XGBoost  | TS%M (2)  | 0.05749002016831224  |
| XGBoost  | FG%M  | 0.07905568941500737  |
| XGBoost  | BL%  | 0.0685452455325351  |
| XGBoost  | TOM (2)  | 0.08201537311636418  |
| Logit  | Last 10 (2)  | 0.07698479102489343  |
| Logit  | SOS (2)  | 8.225948138780171e-09  |
| Logit  | SOS  | 3.9270136842266795e-06  |
| SVM  | Margin  | 0.039302231061566766  |
| SVM  | Last 10 (2)  | 0.08885536255630606  |
| SVM  | Last 10  | 0.011280306649566694  |
| SVM  | CGWin% (2)  | 0.05608979710101595  |
| SVM  | SOS (2)  | 7.13719786347017e-07  |
| SVM  | SOS  | 0.0026918549589998522  |

This table gives us data that confirms that Strength of Schedule data is significantly different in cases where the game prediction ends up correct versus cases where the game prediction ends up incorrect. However, it does not confirm a secondary finding where Steals Per Possession (2) and Block % (2) are also indicators. (Although it should be noted that Block % for team 1 does show up in this chart). It is imperative to note that while this indicates statistical significance for Strength of Schedule, a lack of indication (in the case of Block % and Steal/Pos), does not mean there is no statistical significance. It merely means that this specific analysis found no statistical significance. 

## Notes and Limitations 

This project serves primarily as a proof of concept. As in, this method of determining which factors make NCAA Basketball games harder to predict can be replicated in order to designate future games that may be particularly hard to predict. This designation can be used for betting purposes, for media promotion, or general fan knowledge. 

This project is severely limited because the original four models used as data sources are not of professional grade accuracy. Instead, they all have accuracy scores around 70%. To reiterate, the goal of this project was not to create the best model; instead it was to try to discern what factors made a game hard to predict. Replicating this project with better, more accurate models would likely result in more accurate results. 

Another limitation to note is that in order to avoid multicollinearity, some explanatory variables were removed (those with high VIFs). As such, these variables were not candidates to be identified as causes of hard-to-predict games. 

