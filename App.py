# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np

#Set configuration of the app
st.set_page_config('Predictor','favicon.png','wide')

@st.cache(persist=True)
def get_data(path):
    '''Function to get processed data for EDA and to populate controls'''
    
    data = pd.read_csv(path, index_col=0)    
    num_cols = data.select_dtypes(include=['int64','float64']).columns.to_list()
    cat_cols = data.select_dtypes(include='object').columns.to_list()

    limits = {}
    for col in num_cols:
        lim = []
        lim.append(data[col].min())
        lim.append(data[col].max())
        limits[col] = lim
    
    for col in cat_cols:
        values = data[col].unique().tolist()
        values.append('Otro')
        limits[col] = values
    
    return data, limits
    
path = 'processed_data.csv'
data, limits = get_data(path)

#limits['sex'][0]

st.title('Titulo del app')

#['sex', 'town', 'age', 'paes', 'major', 'faculty', 'VR', 'SR', 'AR', 'NA', 'MR', 'CSA', 'habits', 'sch_type']

with st.expander("Set data for prediction"):
    col1, col2 = st.columns(2)
    with col1:
        paes = st.slider("Set student's PAES", limits['paes'][0],limits['paes'][1])
        sex = st.selectbox("Set student's sex", limits['sex'])
    with col2:
        age = st.slider("Set student's age", limits['age'][0],limits['age'][1])
        
with st.expander("Check your prediction:"):
    st.write('your prediction')