# Importing Library
import pandas as pd

# Function of preprocessing dataframe
def preprocess(df, region_df):
    df = df[df['Season'] == 'Summer']
    df = pd.merge(df, region_df, on='NOC', how='left')
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    df['Total'] = df['Gold'] + df['Silver'] + df['Bronze']
    return df

