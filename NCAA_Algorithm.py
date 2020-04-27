
# coding: utf-8

# In[1]:


# LIBRARIES USED, ALSO REMOVED WARNINGS
import pandas as pd
import numpy as np
import math
import warnings; warnings.simplefilter('ignore')

# CURRENT YEAR DATA - needed for predict matchup
Data2018 = pd.read_csv('2018.csv')
# WEIGHTS - includes all historical weight data
weights = pd.read_csv('weights.csv')
# RESULTS - the results (from last year) we want to use in order to make new weights
# Clean up results
results = pd.read_csv('results.csv')
results['First'] = results['First'].astype('str')
results = results[results['First'] != 'nan'].reset_index()
# TEAMS - the teams participating in the tournament - to be used to simulate tournament
teams2018 = pd.read_csv('teams2018.csv')
teams2018 = teams2018[['Team', 'Seed', 'Region']]


# In[2]:


# TEST CASE TEAMS
UVA = Data2018.loc[Data2018['Team'] == 'Virginia']
Duke = Data2018.loc[Data2018['Team'] == 'Duke']


# In[3]:


# THIS PREDICTS A MATCHUP BETWEEN TWO TEAMS
def predictMatchup(team1, team2):
    columns = list(team1.columns.values)[1:]
    
    team1Score = 0
    team2Score = 0
        
    for column in columns: 
        weight = weights.mean()[1:][column]
                            
        if team1[column].tolist()[0] > team2[column].tolist()[0]:
            team1Score += weight
            
        if team2[column].tolist()[0] > team1[column].tolist()[0]:
            team2Score += weight
        
    if team1Score > team2Score:
        return team1
    else:
        return team2


# In[4]:


# TEST CASE - UVA VS DUKE
predictMatchup(UVA, Duke)['Team']


# In[5]:


# THIS MAKES A NEW YEAR'S WEIGHTS BASED ON PREVIOUS YEAR MATCHUP DATA
def makeWeights(RESULTS):
    cols = RESULTS.columns.values[3:]
    collect_weights = pd.DataFrame(columns=cols)
    collect_weights.loc[0] = 0
    collect_weights
    ind1 = 0
    ind2 = 1
    stop_iter = len(RESULTS)
    for index, row in RESULTS.iterrows():
        if index == stop_iter - 1:
            break

        # If index is odd
        if index % 2 != 0:
            continue

        winner = pd.DataFrame(row)
        loser = pd.DataFrame(RESULTS.iloc[index + 1])

        cols = loser[ind2].keys()[3:]

        for column in cols:
            if winner[ind1][column] > loser[ind2][column]:
                collect_weights[column] = collect_weights[column] + 1    


        ind2 += 2
        ind1 += 2
    
    collect_weights.iloc[0] = collect_weights.iloc[0] / 63
    return collect_weights


# In[6]:


# TEST CASE MAKING WEIGHTS USING 2018 RESULTS
# Note: Column names have been abstracted in order to protect proprietary information
temp_weights = makeWeights(results)
temp_weights.columns = [''] * 30
temp_weights


# In[7]:


# UPDATE THE WEIGHTS - WHEN WE MAKE NEW WEIGHTS, WE WANT TO UPDATE OUR CUMULATIVE WEIGHTS (USED IN PREDICT MATCHUP)
def updateWeights(WEIGHTS):
    new_weights = weights.append(WEIGHTS)
    new_weights = new_weights.drop(columns="Year")
    return new_weights


# In[8]:


# TEST CASE, ADDING 2018 WEIGHTS AGAIN TO THE CUMULATIVE WEIGHT LIST 
x = makeWeights(results)
temp_weights = updateWeights(x)
temp_weights.columns = [''] * 30
# Note: Column names have been abstracted in order to protect proprietary information
temp_weights


# In[9]:


# HERE WE BREAK UP ALL OUR TEAMS INTO REGIONS
South = teams2018[teams2018['Region'] == 'South']
West = teams2018[teams2018['Region'] == 'West']
East = teams2018[teams2018['Region'] == 'East']
Midwest = teams2018[teams2018['Region'] == 'Midwest']


# In[10]:


# HELPER FUNCTIONS TO PRODUCE THE WINNER OF A TOURNAMENT

def roundof64(region):

    remaining = pd.DataFrame(columns=['Team', 'Seed', 'Region'])
    
    while len(region) > 0:
        team1Name = region.iloc[0]['Team'].strip()
        team2Name = region.iloc[-1]['Team'].strip()
                
        # print(region.index[region['Team'] == team1Name].tolist())
        # print(region.index[region['Team'] == team2Name].tolist())
        
        team1 = Data2018[Data2018['Team'] == team1Name]
        team2 = Data2018[Data2018['Team'] == team2Name]        
        
        winner = predictMatchup(team1, team2)['Team'].values[0]

        add = region[region['Team'] == winner]
        add = pd.DataFrame(add)

        remaining = remaining.append(add) 
        
        region = region[region['Team'] != team1Name]
        region = region[region['Team'] != team2Name]
    
    remaining = remaining.sort_values(by=['Seed'])
    return remaining

def setPaths(region):
    region['32Path'] = ''
    region['16Path'] = 'B'

    region.loc[region['Seed'] == 1, '32Path'] = 'A'
    region.loc[region['Seed'] == 16, '32Path'] = 'A'
    region.loc[region['Seed'] == 8, '32Path'] = 'A'
    region.loc[region['Seed'] == 9, '32Path'] = 'A'
    
    region.loc[region['Seed'] == 5, '32Path'] = 'B'
    region.loc[region['Seed'] == 12, '32Path'] = 'B'
    region.loc[region['Seed'] == 4, '32Path'] = 'B'
    region.loc[region['Seed'] == 13, '32Path'] = 'B'
        
    region.loc[region['Seed'] == 6, '32Path'] = 'C'
    region.loc[region['Seed'] == 11, '32Path'] = 'C'
    region.loc[region['Seed'] == 3, '32Path'] = 'C'
    region.loc[region['Seed'] == 14, '32Path'] = 'C'
    
    region.loc[region['Seed'] == 2, '32Path'] = 'D'
    region.loc[region['Seed'] == 15, '32Path'] = 'D'
    region.loc[region['Seed'] == 7, '32Path'] = 'D'
    region.loc[region['Seed'] == 10, '32Path'] = 'D'
    
    region.loc[region['Seed'] == 1, '16Path'] = 'A'
    region.loc[region['Seed'] == 16, '16Path'] = 'A'
    region.loc[region['Seed'] == 8, '16Path'] = 'A'
    region.loc[region['Seed'] == 9, '16Path'] = 'A'
    
    region.loc[region['Seed'] == 5, '16Path'] = 'A'
    region.loc[region['Seed'] == 12, '16Path'] = 'A'
    region.loc[region['Seed'] == 4, '16Path'] = 'A'
    region.loc[region['Seed'] == 13, '16Path'] = 'A'
    
    return region

def roundof32(region):
    region = setPaths(region)
    paths = ['A', 'B', 'C', 'D']
    
    remaining = pd.DataFrame(columns=['Team', 'Seed', 'Region', '32Path', '16Path'])
    
    while len(paths) > 0:
        
        team1Name = region.loc[region['32Path'] == paths[0]].iloc[0]['Team']
        team1 = Data2018[Data2018['Team'] == team1Name]
        
        team2Name = region.loc[region['32Path'] == paths[0]].iloc[1]['Team']
        team2 = Data2018[Data2018['Team'] == team2Name]
               
        winner = predictMatchup(team1, team2)['Team'].values[0]
        add = region[region['Team'] == winner]
        add = pd.DataFrame(add)

        remaining = remaining.append(add)
        
        del paths[0]
    
    return remaining
   
    
def roundof16(region):
    region = setPaths(region)
    paths = ['A', 'B']
    
    remaining = pd.DataFrame(columns=['Team', 'Seed', 'Region', '32Path', '16Path'])
    
    while len(paths) > 0:
        
        team1Name = region.loc[region['16Path'] == paths[0]].iloc[0]['Team']
        team1 = Data2018[Data2018['Team'] == team1Name]
        
        team2Name = region.loc[region['16Path'] == paths[0]].iloc[1]['Team']
        team2 = Data2018[Data2018['Team'] == team2Name]
               
        winner = predictMatchup(team1, team2)['Team'].values[0]
        add = region[region['Team'] == winner]
        add = pd.DataFrame(add)

        remaining = remaining.append(add)
        
        del paths[0]
    
    return remaining

def elite8(region):
    team1Name = region.iloc[0]['Team']
    team1 = Data2018[Data2018['Team'] == team1Name]
        
    team2Name = region.iloc[1]['Team']
    team2 = Data2018[Data2018['Team'] == team2Name]
               
    winner = predictMatchup(team1, team2)
    
    return winner

def simRegion(region):
    x = roundof64(region)
    y = roundof32(x)
    z = roundof16(y)
    return elite8(z)

def seeWinner(mid, east, west, south):
    MIDWEST = simRegion(mid)
    EAST = simRegion(east)
    WEST = simRegion(west)
    SOUTH = simRegion(south)
    
    finalFour1 = predictMatchup(EAST, WEST)
    finalFour2 = predictMatchup(MIDWEST, SOUTH)
    
    winner = predictMatchup(finalFour1, finalFour2)
    return winner


# In[11]:


x = roundof64(Midwest)
y = roundof32(x)
z = roundof16(y)


# In[12]:


temp_winner = seeWinner(Midwest, East, West, South)
temp_winner.columns = [''] * 31
# Note: Column names have been abstracted in order to protect proprietary information
temp_winner


# In[13]:


# FUNCTIONS TO SIMULATE THE TOURNAMENT AND GIVE ROUND BY ROUND INFO

def see32(mid, east, west, south):
    
    MID = roundof64(Midwest)
    # y = roundof32(x)
    # z = roundof16(y)
    
    EAST = roundof64(east)
    # y = roundof32(x)
    # z = roundof16(y)
    
    WEST = roundof64(west)
    # y = roundof32(x)
    # z = roundof16(y)
    
    SOUTH = roundof64(south)
    # y = roundof32(x)
    # z = roundof16(y)
    
    print('######################################################################')
    print('ROUND OF THIRTY TWO')
    print(MID)
    print('----------------------------------------')
    print(EAST)
    print('----------------------------------------')
    print(WEST)
    print('----------------------------------------')
    print(SOUTH)

def see16(mid, east, west, south):
    MID1 = roundof64(Midwest)
    MID = roundof32(MID1)
    # z = roundof16(y)
    
    EAST1 = roundof64(east)
    EAST = roundof32(EAST1)
    # z = roundof16(y)
    
    WEST1 = roundof64(west)
    WEST = roundof32(WEST1)
    # z = roundof16(y)
    
    SOUTH1 = roundof64(south)
    SOUTH = roundof32(SOUTH1)
    # z = roundof16(y)
    
    print('######################################################################')
    print('SWEET SIXTEEN')
    print(MID)
    print('----------------------------------------')
    print(EAST)
    print('----------------------------------------')
    print(WEST)
    print('----------------------------------------')
    print(SOUTH)  
    
def see8(mid, east, west, south):
    MID1 = roundof64(Midwest)
    MID2 = roundof32(MID1)
    MID = roundof16(MID2)
    
    EAST1 = roundof64(east)
    EAST2 = roundof32(EAST1)
    EAST = roundof16(EAST2)
    
    WEST1 = roundof64(west)
    WEST2 = roundof32(WEST1)
    WEST = roundof16(WEST2)
    
    SOUTH1 = roundof64(south)
    SOUTH2 = roundof32(SOUTH1)
    SOUTH = roundof16(SOUTH2)
    
    print('######################################################################')
    print('ELITE EIGHT')
    print(MID)
    print('----------------------------------------')
    print(EAST)
    print('----------------------------------------')
    print(WEST)
    print('----------------------------------------')
    print(SOUTH)  
    
def see4(mid, east, west, south):
    MID1 = roundof64(Midwest)
    MID2 = roundof32(MID1)
    MID3 = roundof16(MID2)
    MID = elite8(MID3)
    
    EAST1 = roundof64(east)
    EAST2 = roundof32(EAST1)
    EAST3 = roundof16(EAST2)
    EAST = elite8(EAST3)

    
    WEST1 = roundof64(west)
    WEST2 = roundof32(WEST1)
    WEST3 = roundof16(WEST2)
    WEST = elite8(WEST3)

    
    SOUTH1 = roundof64(south)
    SOUTH2 = roundof32(SOUTH1)
    SOUTH3 = roundof16(SOUTH2)
    SOUTH = elite8(SOUTH3)

    
    print('######################################################################')
    print('FINAL FOUR')
    print(MID['Team'])
    print('----------------------------------------------------')
    print(EAST['Team'])
    print('----------------------------------------------------')
    print(WEST['Team'])
    print('----------------------------------------------------')
    print(SOUTH['Team'])  

    
def seeChamp(mid, east, west, south):    
    MIDWEST = simRegion(mid)
    EAST = simRegion(east)
    WEST = simRegion(west)
    SOUTH = simRegion(south)
    
    finalFour1 = predictMatchup(EAST, WEST)
    finalFour2 = predictMatchup(MIDWEST, SOUTH)
    
    print('######################################################################')
    print('CHAMPIONSHIP')
    print(finalFour1['Team'])
    print(finalFour2['Team'])

    
    winner = predictMatchup(finalFour1, finalFour2)
    
    print('######################################################################')
    print('WINNER')
    
    print(winner['Team'])
    
    
def simTournament(mid, east, west, south):
    see32(mid, east, west, south)
    see16(mid, east, west, south)
    see8(mid, east, west, south)
    see4(mid, east, west, south)
    seeChamp(mid, east, west, south)


# In[14]:


# SIMULATE THE ENTIRE TOURNAMENT

simTournament(Midwest, East, West, South)

