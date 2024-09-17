# Importing Library
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Module Importing
import preprocessor, helper

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
    country, years = helper.country_and_year(df)
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
        sport_name = helper.sports(df)
        st.header('Most Successful Athlets')
        selected_sports = st.selectbox('Select Sports', sport_name)
        gold_medal_tally = helper.filter_gold_medal_tally(df, selected_sports)
        st.table(gold_medal_tally)

    # Line plot of No of Nations over the Years
    with st.container(border=True):
        nations_over_time = helper.graph_over_time(df, 'region')
        fig = plt.figure(figsize=(10, 5))
        #sns.set_style("whitegrid")
        custom_params = {"axes.spines.right": False, "axes.spines.top": False}
        sns.set_theme(style="white", palette='Spectral', rc=custom_params)
        sns.lineplot(data=nations_over_time, x="Edition", y="No of Regions")
        st.header('Number of Participating Nations over the Years')
        st.pyplot(fig)

    # Line plot of No of Events over the Years
    with st.container(border=True):
        events_over_time = helper.graph_over_time(df, 'Event')
        fig = plt.figure(figsize=(10, 5))
        sns.lineplot(data=events_over_time, x="Edition", y="No of Events")
        st.header('Number of Events over the Years')
        st.pyplot(fig)

    # Line plot of No of Medals over the Years
    with st.container(border=True):
        medal_over_time = df.groupby('Year')['Total'].sum().reset_index()
        medal_over_time.rename(columns={'Year': 'Edition', 'Total': 'Total Medal'}, inplace=True)
        fig = plt.figure(figsize=(10, 5))
        sns.lineplot(medal_over_time, x='Edition', y='Total Medal')
        st.header('Number of Medals over the Years')
        st.pyplot(fig)

    # Line plot of No of Participating Athlets based on Gender over the Years
    with st.container(border=True):
        perticipation_over_time_by_gender = df.groupby(['Year', 'Sex'])['Name'].nunique().reset_index()
        perticipation_over_time_by_gender.rename(columns={'Year': 'Edition', 'Name': 'No of Perticipants'}, inplace=True)
        fig = plt.figure(figsize=(10, 5))
        sns.lineplot(perticipation_over_time_by_gender, x='Edition', y='No of Perticipants', hue='Sex')
        st.header('Number of Perticipating Athlets based on Gender over the Years')
        st.pyplot(fig)

    # Bar plot of The average age of athletes has changed over time
    with st.container(border=True):
        avg_age_over_time = round(df.groupby(['Year', 'Sex'])['Age'].mean()).reset_index()
        avg_age_over_time.rename(columns={'Year': 'Edition', 'Age': 'Average Age'}, inplace=True)
        fig = plt.figure(figsize=(10, 5))
        sns.barplot(avg_age_over_time, x='Edition', y='Average Age', hue='Sex')
        plt.xticks(rotation=90)
        st.header('The average age of athletes has changed over time')
        st.pyplot(fig)

    # Heatmap of No of Events in every Sports over the Years
    with st.container(border=True):
        fig = plt.figure(figsize=(20, 13))
        x = df.drop_duplicates(['Year', 'Event', 'Sport'])
        sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
        plt.xticks(rotation=90)
        st.header('No of Events in every Sports over the Years')
        st.pyplot(fig)

