import pandas as pd

def preprocess(df, region_df):
    df = df[df['Season'] == 'Summer']
    df = pd.merge(df, region_df, on='NOC', how='left')
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df

