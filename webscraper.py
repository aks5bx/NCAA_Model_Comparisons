## Importing libraries for webscraping and dataframe handling
import requests
from bs4 import BeautifulSoup
import pandas as pd

## This is the website from where statistics are being pulled
## https://www.teamrankings.com/ncb/stats/

## Defining function to retrieve a year's march madness teams
def getTeamsForYear(year): 
    filename = str(year) + '.csv' 
    yearDF = pd.read_csv(filename)
    teams = list(yearDF['Team'])
    return teams


## Get list of stats to scrape
statList = ['effective-field-goal-pct', 'ftm-per-100-possessions', 'offensive-rebounding-pct', 'defensive-rebounding-pct', 'assists-per-fgm', 'effective-possession-ratio', 
            'RPI', 'win-pct-all-games', 'win-pct-close-games', 'SOS', 'Last 10', 'average-scoring-margin',  'offensive-efficiency', 'AdjO', 'defensive-efficiency', 'AdjD','EffM', 'AdjEM', 'points-per-game', 'opponent-points-per-game', 'PFAM', 'true-shooting-percentage', 'opponent-true-shooting-percentage', 'TS%M', 'shooting-pct', 'opponent-shooting-pct', 'FG%M', 'three-point-pct', 'free-throw-pct', 'total-rebounding-percentage', 'steals-perpossession', 'turnovers-per-possession', 'opponent-turnovers-per-possession', 'TOM', 'block-pct', 'personal-fouls-per-possession']

## Adding year and team as columns, creating a dataframe with a column for each stat
columnsToUse = ['Year', 'Team'] + statList
collectorDF = pd.DataFrame(columns = columnsToUse)

## Looping through each year for which we have data (2008 - 2019)
for year in range(2008, 2020): 
    ## Creating a new variable for year, technical debt
    currentYear = year
    
    ## Grabbing all the march madness teams of this year
    teamsThisYear = getTeamsForYear(currentYear)
    teamsThisYear = teamsThisYear[:-1]

    ## Initialize empty dataframe
    columnsToUse = ['Year', 'Team'] + statList
    yearDF = pd.DataFrame(columns = columnsToUse)

    ## Status update for the Loop 
    print('CURRENT YEAR :', currentYear)

    yearDF['Team'] = teamsThisYear; yearDF['Year'] = currentYear

    ## Loop through all the stats we want to collect
    for stat in statList: 
        ## Status update for loop
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
        for row in rows:
            cols=row.find_all('td')
            cols=[x.text.strip() for x in cols]
            
            ## If we are looking at data from a march madness team for this year, add it to our DF
            if cols[1] in teamsThisYear: 
                statistic = cols[2]
                yearDF.loc[yearDF.Team == cols[1], stat] = statistic

    ## Append the current year's dataframe to our main dataframe to collect information for each year
    collectorDF = collectorDF.append(yearDF)


## Write dataframe to csv
collectorDF.to_csv('collectorDF.csv')

## NOTE FOR THE END TO END PROCESS: 
## collectorDF will have some data manually added, and will eventually become fullData






