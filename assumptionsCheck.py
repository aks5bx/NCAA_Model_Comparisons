### ASSUMPTIONS ###

# Ordinal Dependent Variable (binary)           (Y) 
# Independent Observations                      (Y) 
# No multicollinearity (!!!)                    (X)
# Data is suitable for log odds relationship    (Y) 

## Import useful libraries
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from tqdm import tqdm
import numpy as np

## Read in data
feedToModelData = pd.read_csv('feedToModelData.csv', index_col = 0)
feedToModelData.iloc[:,2:-1].corr().to_csv('correlationMatrix.csv')


### The work here is designed to correct the multicollinearity assumption, 
### which is currently being violated 

## Define function to calculate Variable Inflation Factor
def calc_vif(X):
    # Calculating VIF
    vif = pd.DataFrame()
    vif["variables"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

    return(vif)

for i in tqdm(range(1, 751)): 
    try: 
        ## Run function to produce VIFs
        X = feedToModelData.iloc[:i,2:-1]
        calc_vif(X)

    except: 
        print('error')
        feedToModelData = feedToModelData.drop(i - 1)

val = 1000000
i = 0

feedToModelDataLoop = feedToModelData
feedToModelDataLoop = feedToModelDataLoop.loc[:, feedToModelDataLoop.columns != 'Team1Win']
while val > 100: 
    i += 1
    dfSource = calc_vif(feedToModelDataLoop)
    dfSource = dfSource[~dfSource.isin([np.nan, np.inf, -np.inf]).any(1)]
    VIFDF = pd.DataFrame(dfSource)
    VIFDF = VIFDF.sort_values(by = 'VIF', ascending = False).reset_index(drop = True)
    
    
    val = VIFDF.iloc[0]['VIF']
    
    VIFDF = VIFDF.iloc[1:]
        
    variables = list(VIFDF['variables'])
    
    feedToModelDataLoop = feedToModelDataLoop[variables]

variables = variables + ['Team1Win']
feedToModelData = feedToModelData[variables]

### We now meet the assumption for multicollinearity

# feedToModelData.to_csv('feedToModelData2.csv')














