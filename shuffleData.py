import pandas as pd
from random import sample

data = pd.read_csv('regressionUseData.csv')


#######################################
######### JUMBLE UP DATA ##############
#######################################

team1cols = data.columns[2:39]
team2cols = data.columns[39:76]

samples = sample(list(range(0, 752)), 376)

for index, row in data.iterrows():

    if index in samples: 
        ind = row['Ind']
        year = row['Year']

        team1 = row[team1cols]
        team2 = row[team2cols]

        totalRow = [ind] + [year] + list(team2) + list(team1) + [0]
        data.loc[index:index, : ] = totalRow

data = data.drop('Team', 1)
data = data.drop('Team2', 1)

## THIS SHUFFLES UP THE DATA 
data.to_csv('feedToModelData.csv')
