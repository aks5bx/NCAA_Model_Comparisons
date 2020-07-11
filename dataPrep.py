## Import library for data handling
import pandas as pd

## Read in two data frames 
## matchups - all of the matchup data, so we know which team played which and who won
## fullData - the data for each team and their aggregate statistics
matchups = pd.read_csv('matchups.csv')
fullData = pd.read_csv('fullData.csv')

## Some dataframe handling
matchups = matchups.dropna()
matchups = matchups.reset_index()

## Define a function to retrieve a team's stats based on the year and team name
def getTeamStats(team, year): 
    newDF = fullData[((fullData['Year'] == year) & (fullData['Team'] == team))]
    for index, row in newDF.iterrows():
        return list(row)

## Test of the function
print(getTeamStats('iona', 2019))


# newCols = ['RPI', 'Win%', 'CGWin%', 'SOS', 'Last 10', 'Margin', 'OffE', 'AdjO', 'DefE', 'AdjD', 'EffM', 'AdjEM', 'PF', 'PA', 'PFAM', 'TrueS%', 'OpTS%', 'TS%M', 'FG%', 'OpFG%', 'FG%M', '3P%', 'FT%', 'RB%', 'ST/Pos', 'TO/Pos', 'OpTO/Pos', 'TOM', 'BL%', 'PF/Pos']
# statList = ['effective-field-goal-pct', 'ftm-per-100-possessions', 'offensive-rebounding-pct', 'defensive-rebounding-pct', 'assists-per-fgm', 'effective-possession-ratio']
# columnsToUse = ['Seed', 'Year', 'Team'] + statList
# allCols = columnsToUse + newCols
# allCols = allCols + allCols

# regressionData = pd.DataFrame(columns = allCols)

## Generating an empty list for collection purposes 
regressionData = []

## Declaring variables outside of the loop to track progress of the loop
failureTotal = 0
successTotal = 0
i = 0

## Using the csv of teams and their stats (matchups and fullData) to produce data that is usable for a regression/other ML algorithm 
## the csv will have winning team and the losing team on the same line, with the result as its own column
## For each row in matchups
for index, row in matchups.iterrows():
    ## Because of the way the data is formatted - every third row we are ready to read in a new matchup
    if i % 3 == 0: 
        
        ## The first team is always the winner, so we grab that first
        year = int(row['Year'])
        winner = row['Team'].strip()
        winnerInfo = getTeamStats(winner, year)

        ## The next row will be the losing team
        nextRow = matchups.iloc[index + 1]

        loser = nextRow['Team'].strip()
        loserInfo = getTeamStats(loser, year)            

        # Combining the data into one row and append it to our list of matchups
        try:
            totalData = winnerInfo + loserInfo 
            regressionData.append(totalData)
            successTotal += 1
        except: 
            failureTotal += 1
            print('failure', i, winner, loser, year)

    i += 1

## Report the accuracy of this process - there may be some edge case failures
print(round(failureTotal / (failureTotal + successTotal), 4) * 100, '%')

## Transform list of matchups into a dataframe, write it to a csv
regressionDF = pd.DataFrame.from_records(regressionData)
regressionDF.to_csv('regressionData.csv')


## NOTE FOR THE END TO END PROCESS: 
## regressionData gets changed and manually cleaned to turn into regressionUseData 


