# Importing Library
import numpy as np

# Function for making the list of country and year
def country_and_year(df):
    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')

    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    return country, years

# Function for making the list of sports
def sports(df):
    sport = df['Sport'].unique().tolist()
    sport.sort()
    sport.insert(0, 'Overall')

    return sport

# Filtering Function of medal Tally
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

# Filtering function of nations and events over the years
def graph_over_time(df, var):
    data_over_time = df.drop_duplicates(['Year', var]).groupby('Year')[var].nunique().reset_index()
    data_over_time.rename(columns={'Year': 'Edition', var: f'No of {var.capitalize()+'s'}'}, inplace=True)
    return data_over_time

# Filtering function of most successful athlets
def filter_gold_medal_tally(df, sport):
    temp_df = df[df['Medal'] == 'Gold'][['Name', 'Sport']].value_counts()
    temp_df = temp_df.reset_index().rename(columns={'Name': 'Athlete', 'count': 'No of Gold Medal'})
    if sport == 'Overall':
        gold_medal_tally = temp_df
    if sport != 'Overall':
        gold_medal_tally = temp_df[(temp_df['Sport'] == sport)]

    gold_medal_tally.index = np.arange(1, len(gold_medal_tally) + 1)

    return gold_medal_tally.head(10)