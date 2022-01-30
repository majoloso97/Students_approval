# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#from jupyterthemes import jtplot

# choose which theme to inherit plotting style from
# onedork | grade3 | oceans16 | chesterish | monokai | solarizedl | solarizedd
#jtplot.style(theme='chesterish')

rc={'figure.facecolor':'#0f1420',
    'xtick.color':'#ebebeb',
    'ytick.color':'#ebebeb',
    'axes.labelcolor':'#ebebeb',
    'text.color':'#ebebeb',
    'figure.figsize':(3,3)}

sns.set_theme(palette='dark', rc=rc)

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

st.title('Titulo del app')

#['sex', 'town', 'age', 'paes', 'major', 'faculty', 'VR', 'SR', 'AR', 'NA', 'MR', 'CSA', 'habits', 'sch_type']

with st.expander("Set data for prediction"):
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(sns.catplot(x='sex',y='paes',data=data,kind='bar'))
        paes = st.slider("Set student's PAES", float(limits['paes'][0]),float(limits['paes'][1]))
        sex = st.selectbox("Set student's sex", limits['sex'])
    with col2:
        age = st.slider("Set student's age", float(limits['age'][0]),float(limits['age'][1]))
        
with st.expander("Check your prediction:"):
    st.write('your prediction')
    
    
    
    
    
    
    