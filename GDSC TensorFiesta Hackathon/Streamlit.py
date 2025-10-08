import numpy as np
import pandas as pd
import streamlit as st
from pandas_profiling import ProfileReport
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from streamlit_option_menu import option_menu
import google.generativeai as genai
import os
ds = pd.read_csv("Mod_Reviews_data.csv")
Price_review = ds[['PRICE_RATING','Review_result']]



# Web App Title
st.markdown('''
# **Reviews Analyser**
---
''')

# Upload CSV data
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/dataprofessor/data/master/delaney_solubility_with_descriptors.csv)
""")
    

with st.sidebar:
    selected = option_menu(
        menu_title="2. Select a page",
        options = ['Overview','Text analytics','Graphs','Example Review'],
        default_index=0
    )
if selected == 'Overview':
    st.subheader(" Overview")
    try:
        def load_csv():
            csv = pd.read_csv(uploaded_file)
            return csv
        df = load_csv()
        pr = ProfileReport(df, explorative=True,dark_mode=True)
        st.header('**Input DataFrame**')
        st.write(df)
        st.write('---')
        st.header('**Pandas Profiling Report**')
        st_profile_report(pr)
    except :
        st.write('Upload a file')
if selected == 'Text analytics':
    st.subheader(" Text analytics")
    st.write("### Review Results")
    st.write(ds['Review_result'].value_counts())
    st.write("### Review Result for its price")
    st.write(ds[['PRICE_RATING','Review_result']].value_counts())
    st.write("### Graph of distribution of reviews")
    st.bar_chart(ds['Review_result'].head(100),width=50)
if selected == 'Graphs':
    st.subheader(" Graphs of the following dataset")
    st.write("### Graph of Price Rating")
    st.bar_chart(ds['PRICE_RATING'].value_counts())
    st.write("### Graph of Value Rating")
    st.bar_chart(ds['VALUE_RATING'].value_counts())
    st.write("### Graph of Quality Rating")
    st.bar_chart(ds['QUALITY_RATING'].value_counts())
    st.write("### Graph of number of product sold to states")
    st.bar_chart(ds['STATES'].value_counts())
    st.write("### Graph of ndistribution of prices")
    st.bar_chart(ds['PRICE'].value_counts())
if selected == 'Example Review': 
    st.subheader("Analysing the review")
    Review = st.text_input("Enter a review") 
    os.environ['GOOGLE_API_KEY2'] = "AIzaSyBFS_r8LkL327zLGyru-jB2q3Q31KfCt1E"
    genai.configure(api_key=os.environ['GOOGLE_API_KEY2'])
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(' Classify ' + '"' + str(Review) + '"' + ' as positive negative or neutral . Give output only in one word . nan is neutral').text
    st.success(response)  
