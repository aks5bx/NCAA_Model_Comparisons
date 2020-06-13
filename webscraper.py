import requests
from bs4 import BeautifulSoup
import pandas as pd

## Define DataFrame
## https://www.teamrankings.com/ncb/stats/

def getTeamsForYear(year): 
    filename = str(year) + '.csv' 
    yearDF = pd.read_csv(filename)
    teams = list(yearDF['Team'])
    return teams

def listDiff(li1, li2): 
    res = list(set(li1) - set(li2))
    return res

## Get list of stats to scrape
statList = ['effective-field-goal-pct', 'ftm-per-100-possessions', 'offensive-rebounding-pct', 'defensive-rebounding-pct', 'assists-per-fgm', 'effective-possession-ratio', 
            'RPI', 'win-pct-all-games', 'win-pct-close-games', 'SOS', 'Last 10', 'average-scoring-margin',  'offensive-efficiency', 'AdjO', 'defensive-efficiency', 'AdjD','EffM', 'AdjEM', 'points-per-game', 'opponent-points-per-game', 'PFAM', 'true-shooting-percentage', 'opponent-true-shooting-percentage', 'TS%M', 'shooting-pct', 'opponent-shooting-pct', 'FG%M', 'three-point-pct', 'free-throw-pct', 'total-rebounding-percentage', 'steals-perpossession', 'turnovers-per-possession', 'opponent-turnovers-per-possession', 'TOM', 'block-pct', 'personal-fouls-per-possession']

newCols = ['RPI', 'Win%', 'CGWin%', 'SOS', 'Last 10', 'Margin', 'OffE', 'AdjO', 'DefE', 'AdjD', 'EffM', 'AdjEM', 'PF', 'PA', 'PFAM', 'TrueS%', 'OpTS%', 'TS%M', 'FG%', 'OpFG%', 'FG%M', '3P%', 'FT%', 'RB%', 'ST/Pos', 'TO/Pos', 'OpTO/Pos', 'TOM', 'BL%', 'PF/Pos']


columnsToUse = ['Year', 'Team'] + statList
collectorDF = pd.DataFrame(columns = columnsToUse)

for year in range(2008, 2020): 
    ## Get relevant teams for this year
    currentYear = year

    teamsThisYear = getTeamsForYear(currentYear)
    teamsThisYear = teamsThisYear[:-1]

    ## Initialize empty dataframe
    columnsToUse = ['Year', 'Team'] + statList
    yearDF = pd.DataFrame(columns = columnsToUse)


    ## Determine the year we are looking at 
    print('CURRENT YEAR :', currentYear)

    ## Website stats lags a year so year = year -1 
    yearDF['Team'] = teamsThisYear; yearDF['Year'] = currentYear

    ## Determine the stat that we want to grab
    for stat in statList: 
        print(stat)
        ## Define Dictionary
        statDict = {}
        ## Webscrape 
        year = str(year)
        URL = 'https://www.teamrankings.com/ncaa-basketball/stat/' + stat + '?date=' + year + '-04-10'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        table_body=soup.find('tbody')
        try: 
            rows = table_body.find_all('tr')
        except:
            print('failure ', stat)
            continue

        ## Parse data
        success = False
        for row in rows:
            cols=row.find_all('td')
            cols=[x.text.strip() for x in cols]

            if cols[1] in teamsThisYear: 
                statistic = cols[2]
                yearDF.loc[yearDF.Team == cols[1], stat] = statistic

    yearDF.to_csv('2019Check.csv')


    collectorDF = collectorDF.append(yearDF)

    if year == 2019: 
        print(yearDF)

collectorDF.to_csv('collectorDF.csv')

## COLLECTORDF will have some data manually added, and will eventually become fullData

'''

newCols = ['RPI', 'Win%', 'CGWin%', 'SOS', 'Last 10', 'Margin', 'OffE', 'AdjO', 'DefE', 'AdjD', 'EffM', 'AdjEM', 'PF', 'PA', 'PFAM', 'TrueS%', 'OpTS%', 'TS%M', 'FG%', 'OpFG%', 'FG%M', '3P%', 'FT%', 'RB%', 'ST/Pos', 'TO/Pos', 'OpTO/Pos', 'TOM', 'BL%', 'PF/Pos']

allCols = columnsToUse + newCols

collector2 = pd.DataFrame(columns = allCols)

# print(collectorDF.loc[collectorDF['Year'] == 2008])

for year in range(2019, 2020): 
    print(year)
    filename = str(year) + '.csv'
    currentYearDF = pd.read_csv(filename)
    yearMergeDF = collectorDF[(collectorDF['Year'] == year)]

    # res = yearMergeDF.merge(currentYearDF)
    res = pd.merge(left = yearMergeDF, right = currentYearDF, how='outer', left_on = 'Team', right_on = 'Team')

    print(collector2.columns)

    collector2 = collector2.append(res)  

collector2.to_csv('fullData2.csv')
'''




