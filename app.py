import streamlit as st
import pandas as pd
import preprocessor, helper
from helper import *

df = pd.read_csv('data/athlete_events.csv')
region_df = pd.read_csv('data/noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

user_menu = st.sidebar.radio(
    "Select an option",
    ("Medal Tally", "Overall Analysis", "Country-wise Analysis", "Athlete-wise Analysis")
)


if user_menu == 'Medal Tally':
    country, years = helper.country_and_year(df)
    selected_year = st.sidebar.selectbox('Select Year: ', years)
    selected_country = st.sidebar.selectbox('Select Country: ', country)
    medal_tally = helper.filter_medal(df, selected_year, selected_country)
    st.header('Medal Tally')
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f'Medal Tally in {selected_year} Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f'Medal Tally of {selected_country} in all Olympics')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(f'Medal Tally of {selected_country} in {selected_year} Olympics')
    st.table(medal_tally)