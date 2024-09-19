# Importing Library
import numpy as np

# Function for making the list of filtering
def list_maker(df, var):
    if df[var].isnull().any():
        new_list = df[var].dropna().unique().tolist()
    else:
        new_list = df[var].unique().tolist()

    new_list.sort()
    new_list.insert(0, 'Overall')

    return new_list

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
    return data_over_time

# Filtering (sports wize) function of most successful athlets
def filter_gold_medal_tally_by_sports(df, sport):
    temp_df = df[df['Medal'] == 'Gold'][['Name', 'Sport']].value_counts()
    temp_df = temp_df.reset_index().rename(columns={'Name': 'Athlete', 'count': 'No of Gold Medal'})
    if sport == 'Overall':
        gold_medal_tally = temp_df
    if sport != 'Overall':
        gold_medal_tally = temp_df[(temp_df['Sport'] == sport)]

    gold_medal_tally.index = np.arange(1, len(gold_medal_tally) + 1)

    return gold_medal_tally.head(10)

# Filtering (country wize) function of most successful athlets
def filter_gold_medal_tally_by_country(df, country):
    temp_df = df[df['Medal'] == 'Gold'][['Name', 'Sport', 'region']].value_counts()
    temp_df = temp_df.reset_index() #.rename(columns={'Name': 'Athlete', 'count': 'No of Gold Medal'})
    if country == 'Overall':
        gold_medal_tally = temp_df
    if country != 'Overall':
        gold_medal_tally = temp_df[(temp_df['region'] == country)]

    gold_medal_tally.index = np.arange(1, len(gold_medal_tally) + 1)

    return gold_medal_tally.head(10)

# Filtering function top 10 countries based on medal
def top_10_country(df):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year', 'City','Sport','Event','Medal'])
    medal_df = medal_df.dropna(subset=['Medal'])
    top_10_country = medal_df.groupby('region')['Medal'].count().reset_index().nlargest(10, 'Medal')['region']
    top_10_medal_df = medal_df[medal_df['region'].isin(top_10_country)]
    return top_10_country, top_10_medal_df

# Filtering function of medal over time by country
def medal_over_time_by_country(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team','NOC','Games','Year', 'City','Sport','Event','Medal'])
    if country == 'Overall':
        medal_over_time = temp_df
    if country != 'Overall':
        medal_over_time = temp_df[temp_df['region'] == country]
    medal_over_time = medal_over_time.groupby('Year')['Medal'].count().reset_index()
    medal_over_time['Year'].astype('int')
    medal_over_time['Medal'].astype('int')

    return  medal_over_time

# Filtering function of Medal won in sports over Time
def medal_in_sports_over_time_by_country(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team','NOC','Games','Year', 'City','Sport','Event','Medal'])
    if country == 'Overall':
        medal_in_sports_over_time = temp_df
    if country != 'Overall':
        medal_in_sports_over_time = temp_df[temp_df['region'] == country]
    pt = medal_in_sports_over_time.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int')

    return  pt