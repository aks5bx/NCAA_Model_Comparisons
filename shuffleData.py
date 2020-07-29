## Importing useful libraries
import pandas as pd
from random import sample

data = pd.read_csv('regressionUseData.csv')


#######################################
######### JUMBLE UP DATA ##############
####################################### 

## Separate team 1 and team 2 data
team1cols = data.columns[2:39]
team2cols = data.columns[39:76]

## Generate random rows to shuffle data
samples = sample(list(range(0, 752)), 376)

## For each row
for index, row in data.iterrows():
    
    ## If the row was randomly selected
    if index in samples: 
        
        ## Make it such that team 1 and team 2 switches, so team 2 becomes team 1
        ind = row['Ind']
        year = row['Year']

        team1 = row[team1cols]
        team2 = row[team2cols]

        totalRow = [ind] + [year] + list(team2) + list(team1) + [0]
        data.loc[index:index, : ] = totalRow

## Drop extraneous columns
data = data.drop('Team', 1)
data = data.drop('Team2', 1)

## write shuffled data to csv 
data.to_csv('feedToModelData.csv')
