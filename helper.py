import numpy as np

def country_and_year(df):
    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')

    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    return country, years

def filter_medal(df, year, country):
    flag = 0
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_tally
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_tally[medal_tally['Year'] == int(year)]
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_tally[medal_tally['region'] == country]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_tally[(medal_tally['Year'] == int(year)) & (medal_tally['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Year').reset_index().rename(columns={'region': 'Region'})
    else:
        x = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False).reset_index().rename(columns={'region': 'Region'})
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x.index = np.arange(1, len(x) + 1)

    return x