import pandas as pd

matchups = pd.read_csv('matchups.csv')
fullData = pd.read_csv('fullData.csv')

matchups = matchups.dropna()
matchups = matchups.reset_index()

# print(matchups.iloc[396])

def getTeamStats(team, year): 
    newDF = fullData[((fullData['Year'] == year) & (fullData['Team'] == team))]
    for index, row in newDF.iterrows():
        return list(row)


print(getTeamStats('iona', 2019))


# newCols = ['RPI', 'Win%', 'CGWin%', 'SOS', 'Last 10', 'Margin', 'OffE', 'AdjO', 'DefE', 'AdjD', 'EffM', 'AdjEM', 'PF', 'PA', 'PFAM', 'TrueS%', 'OpTS%', 'TS%M', 'FG%', 'OpFG%', 'FG%M', '3P%', 'FT%', 'RB%', 'ST/Pos', 'TO/Pos', 'OpTO/Pos', 'TOM', 'BL%', 'PF/Pos']
# statList = ['effective-field-goal-pct', 'ftm-per-100-possessions', 'offensive-rebounding-pct', 'defensive-rebounding-pct', 'assists-per-fgm', 'effective-possession-ratio']
# columnsToUse = ['Seed', 'Year', 'Team'] + statList
# allCols = columnsToUse + newCols
# allCols = allCols + allCols

# regressionData = pd.DataFrame(columns = allCols)
regressionData = []

failureTotal = 0
successTotal = 0
i = 0

## Use the csv of teams and their stats to produce regression ready csv 
## the csv will have winning team and the losing team on the same line
for index, row in matchups.iterrows():
    if i % 3 == 0: 

        year = int(row['Year'])
        winner = row['Team'].strip()
        winnerInfo = getTeamStats(winner, year)

        nextRow = matchups.iloc[index + 1]

        loser = nextRow['Team'].strip()
        loserInfo = getTeamStats(loser, year)            

        try:
            totalData = winnerInfo + loserInfo 
            regressionData.append(totalData)
            successTotal += 1
        except: 
            failureTotal += 1
            print('failure', i, winner, loser, year)

    i += 1


print(round(failureTotal / (failureTotal + successTotal), 4) * 100, '%')

regressionDF = pd.DataFrame.from_records(regressionData)
regressionDF.to_csv('regressionData.csv')

## REGRESSIONDATA gets changed and manually cleaned to turn into REGRESSIONUSEDATA