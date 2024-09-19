# Importing Library
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Module Importing
import preprocessor, helper
from helper import medal_over_time_by_country, filter_medal

df = pd.read_csv('./data/athlete_events.csv')
region_df = pd.read_csv('./data/noc_regions.csv')

df = preprocessor.preprocess(df, region_df)
st.set_page_config(
    page_title='Olympic Data Insights',
    page_icon='./favicon.png',
    layout = 'wide',
    initial_sidebar_state = 'auto'
)
st.sidebar.title('Olympic Data Insights')
st.sidebar.link_button("Dataset", "https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results")
user_menu = st.sidebar.radio(
    "Select an option",
    ("Medal Tally", "Overall Analysis", "Country-wise Analysis", "Athlete-wise Analysis")
)

# Medal Tally
if user_menu == 'Medal Tally':
    country = helper.list_maker(df, 'region')
    years = helper.list_maker(df, 'Year')
    selected_year = st.sidebar.selectbox('Select Year: ', years)
    selected_country = st.sidebar.selectbox('Select Country: ', country)
    medal_tally = helper.filter_medal(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.header('Overall Medal Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.header(f'Medal Tally in {selected_year} Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.header(f'Medal Tally of {selected_country} in all Olympics')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.header(f'Medal Tally of {selected_country} in {selected_year} Olympics')
    st.table(medal_tally)

# Overall Analysis
if user_menu == 'Overall Analysis':
    # Overall Editions, Events, Sports, Hosts, Athlets, Participating Nations
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        editions = df['Games'].nunique() - 1
        events = df['Event'].nunique()
        sports = df['Sport'].nunique()
        hosts = df['City'].nunique()
        athlets = df['Name'].nunique()
        participating_nations = df['region'].unique().shape[0]

        with col1:
            st.subheader("Editions")
            st.subheader(editions)

        with col2:
            st.subheader("Events")
            st.subheader(events)

        with col3:
            st.subheader("Sports")
            st.subheader(sports)

        st.divider()

        col4, col5, col6 = st.columns(3)
        with col4:
            st.subheader("Hosts")
            st.subheader(hosts)

        with col5:
            st.subheader("Athlets")
            st.subheader(athlets)

        with col6:
            st.subheader("Participating Nations")
            st.subheader(participating_nations)

    # Most Successful Athlets Tally
    with st.container(border=True):
        st.header(f'Most Successful Athlets (Overall)')
        gold_medal_tally = helper.filter_gold_medal_tally_by_sports(df, 'Overall')
        st.table(gold_medal_tally)

    # Count plot of Medal won by countries over time
    top_10_country, top_10_medal_df = helper.top_10_country(df)
    with st.container(border=True):
        fig = plt.figure(figsize=(10, 5))
        custom_params = {"axes.spines.right": False, "axes.spines.top": False}
        sns.set_theme(style="white", palette='Set1', rc=custom_params)
        sns.countplot(top_10_medal_df, x='region', hue='Medal', order=top_10_country)
        plt.title('Total Medals by Top 10 Countries')
        plt.xlabel("Country")
        plt.ylabel('Number of Medals')
        st.pyplot(fig)

    # Count plot of Total Medals won by male and female of Top 10 Country
    with st.container(border=True):
        fig = plt.figure(figsize=(10, 5))
        sns.countplot(top_10_medal_df, x='region', hue='Sex', order=top_10_country)
        plt.title('Total Medals won by Male and Female of Top 10 Countries')
        plt.xlabel("Country")
        plt.ylabel('Number of Medals')
        st.pyplot(fig)

    # Line plot of No of Nations over the Years
    with st.container(border=True):
        nations_over_time = helper.graph_over_time(df, 'region')
        fig = plt.figure(figsize=(10, 5))
        sns.lineplot(data=nations_over_time, x="Year", y="region")
        plt.title('Number of Participating Nations over the Years')
        plt.xlabel('Edition')
        plt.ylabel('No of Participation Nations')
        st.pyplot(fig)

    # Line plot of No of Events over the Years
    with st.container(border=True):
        events_over_time = helper.graph_over_time(df, 'Event')
        fig = plt.figure(figsize=(10, 5))
        sns.lineplot(data=events_over_time, x="Year", y="Event")
        plt.xlabel('Edition')
        plt.ylabel('No of Events')
        plt.title('Number of Events over the Years')
        st.pyplot(fig)

    # Line plot of No of Medals over the Years
    with st.container(border=True):
        medal_over_time = df.groupby('Year')['Total'].sum().reset_index()
        fig = plt.figure(figsize=(10, 5))
        sns.lineplot(medal_over_time, x='Year', y='Total')
        plt.title('Number of Medals over the Years')
        plt.xlabel('Edition')
        plt.ylabel('Number of Medals')
        st.pyplot(fig)

    # Line plot of No of Participating Athlets based on Gender over the Years
    with st.container(border=True):
        perticipation_over_time_by_gender = df.groupby(['Year', 'Sex'])['Name'].nunique().reset_index()
        fig = plt.figure(figsize=(10, 5))
        sns.lineplot(perticipation_over_time_by_gender, x='Year', y='Name', hue='Sex')
        plt.title('Number of Perticipating Athlets based on Gender over the Years')
        plt.xlabel('Edition')
        plt.ylabel('No of Perticipants')
        st.pyplot(fig)

    # Heatmap of No of Events in every Sports over the Years
    with st.container(border=True):
        fig = plt.figure(figsize=(20, 13))
        x = df.drop_duplicates(['Year', 'Event', 'Sport'])
        sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
        plt.xticks(rotation=90)
        st.subheader('Number of Events in every Sports over the Years')
        st.pyplot(fig)

# Country wise Analysis
if user_menu == "Country-wise Analysis":
    country_for_medal = helper.list_maker(df, 'region')
    selected_country_for_medal = st.sidebar.selectbox('Select Country: ', country_for_medal)

    # Most Successful Athlets Tally
    with st.container(border=True):
        st.header(f'Most Successful Athlets ({selected_country_for_medal})')
        gold_medal_tally = helper.filter_gold_medal_tally_by_country(df, selected_country_for_medal)
        st.table(gold_medal_tally)

    # Line plot of Total Medals won by Countries over Time
    with st.container(border=True):
        medal_over_time_by_country = helper.medal_over_time_by_country(df, selected_country_for_medal)
        fig = plt.figure(figsize=(10, 5))
        sns.lineplot(medal_over_time_by_country, x='Year', y='Medal')
        plt.title(f'{selected_country_for_medal} performance over the Years')
        plt.xlabel("Year")
        plt.ylabel('Number of Medals')
        st.pyplot(fig)

    # Heatmap of No of Medal won in every Sports over the Years
    with st.container(border=True):
        pt = helper.medal_in_sports_over_time_by_country(df, selected_country_for_medal)
        fig = plt.figure(figsize=(20,15))
        sns.heatmap(pt, annot=True)
        st.header(f'{selected_country_for_medal} performance in every Sports over the Years')
        st.pyplot(fig)

if user_menu == 'Athlete-wise Analysis':
    athlets_df = df.drop_duplicates(subset=['Name', 'region'])

    # Most Successful Athlets Tally
    with st.container(border=True):
        sport_name = helper.list_maker(df, 'Sport')
        st.header(f'Most Successful Athlets')
        selected_sports = st.selectbox('Select Sports', sport_name)
        gold_medal_tally = helper.filter_gold_medal_tally_by_sports(df, selected_sports)
        st.table(gold_medal_tally)

    # Scatter plot of Height vs Weight
    with st.container(border=True):
        st.header('Height vs Weight')
        selected_sport = helper.list_maker(athlets_df, 'Sport')
        selected_sport = st.selectbox('Select Sport: ', selected_sport)
        filter_sport = helper.filter_sport(athlets_df, selected_sport)
        fig = plt.figure(figsize=(10, 5))
        sns.scatterplot(filter_sport, x='Height', y='Weight', hue='Medal', style='Sex')
        st.pyplot(fig)

    # Bar plot of The average age of athletes has changed over time
    with st.container(border=True):
        avg_age_over_time = round(df.groupby(['Year', 'Sex'])['Age'].mean()).reset_index()
        fig = plt.figure(figsize=(10, 5))
        sns.barplot(avg_age_over_time, x='Year', y='Age', hue='Sex')
        plt.title('The average age of athletes has changed over time')
        plt.xticks(rotation=90)
        plt.xlabel('Edition')
        plt.ylabel('Average Age')
        st.pyplot(fig)

    # Filtering Athlets by their corresponded Medal
    gold_medalist = athlets_df[athlets_df['Medal'] == 'Gold']
    silver_medalist = athlets_df[athlets_df['Medal'] == 'Silver']
    bronze_medalist = athlets_df[athlets_df['Medal'] == 'Bronze']

    # Age Distribution of Athlets
    age = athlets_df['Age'].dropna().reset_index()
    with st.container(border=True):
        fig = plt.figure(figsize=(10, 5))
        sns.kdeplot(age, x='Age', label='Overall Age', linewidth=2)
        sns.kdeplot(gold_medalist, x='Age', label='Gold Medalists Age', linewidth=2)
        sns.kdeplot(silver_medalist, x='Age', label='Silver Medalists Age', linewidth=2)
        sns.kdeplot(bronze_medalist, x='Age', label='Bronze Medalists Age', linewidth=2)
        plt.legend()
        plt.title('Age Distribution of Athlets')
        st.pyplot(fig)

    # weight Distribution of Athlets
    weight = athlets_df['Weight'].dropna().reset_index()
    with st.container(border=True):
        fig = plt.figure(figsize=(10, 5))
        sns.kdeplot(weight, x='Weight', label='Overall Weight', linewidth=2)
        sns.kdeplot(gold_medalist, x='Weight', label='Gold Medalists Weight', linewidth=2)
        sns.kdeplot(silver_medalist, x='Weight', label='Silver Medalists Weight', linewidth=2)
        sns.kdeplot(bronze_medalist, x='Weight', label='Bronze Medalists Weight', linewidth=2)
        plt.legend()
        plt.title('Weight Distribution of Athlets')
        st.pyplot(fig)

    # Height Distribution of Athlets
    height = athlets_df['Height'].dropna().reset_index()
    with st.container(border=True):
        fig = plt.figure(figsize=(10, 5))
        sns.kdeplot(height, x='Height', label='Overall Height', linewidth=2)
        sns.kdeplot(gold_medalist, x='Height', label='Gold Medalists Height', linewidth=2)
        sns.kdeplot(silver_medalist, x='Height', label='Silver Medalists Height', linewidth=2)
        sns.kdeplot(bronze_medalist, x='Height', label='Bronze Medalists Height', linewidth=2)
        plt.legend()
        plt.title('Height Distribution of Athlets')
        st.pyplot(fig)






