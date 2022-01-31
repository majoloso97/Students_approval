# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Set custom theme for plots
rc={
    'figure.facecolor':'#0f1420',
    'axes.labelcolor':'#ebebeb',
    'axes.facecolor':'#373a44',
    'xtick.color':'#ebebeb',
    'ytick.color':'#ebebeb',
    'ytick.labelcolor':'#ebebeb',
    'text.color':'#ebebeb'
    }

sns.set_theme(palette='dark', rc=rc)

#Set global configuration of the st app
st.set_page_config('Predictor','favicon.png','wide')

#
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

#App building
st.title('Análisis predictivo de aprobación de estudiantes')

#['sex', 'town', 'age', 'paes', 'major', 'faculty', 'VR', 'SR', 'AR', 'NA', 'MR', 'CSA', 'habits', 'sch_type']

with st.expander('Análisis exploratorio'):
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(sns.catplot(x='sex',y='paes',data=data,kind='bar',palette='colorblind'))
    with col2:
        st.pyplot(sns.catplot(x='sex',y='grade',data=data,kind='bar',palette='colorblind'))
  

def create_imput_widget(variable, var_type='float'):
    widget_label = "Set student's " + variable
    if var_type == 'cat':
        return st.selectbox(widget_label, limits[variable])
    elif var_type == 'int':
        return st.slider(widget_label, int(limits[variable][0]), int(limits[variable][1]))
    else:
        return st.slider(widget_label, float(limits[variable][0]), float(limits[variable][1]))

to_predict = {}

with st.expander('Definición de valores para predecir'):
    c1, c2, c3 = st.columns((5,10,6))
    with c1:
        st.subheader('Variables numéricas')
    with c2:
        st.subheader('Variables categóricas')    
    with c3:
        st.subheader('Variables psicopedagógicas')
    
    col1, col2, col3, col4 = st.columns((5,10,3,3))
    with col1:
        to_predict['age'] = create_imput_widget('age','int')
        to_predict['paes'] = create_imput_widget('paes','float')
        to_predict['habits'] = create_imput_widget('habits','int')
    with col2:
        to_predict['sex'] = create_imput_widget('sex', 'cat')
        to_predict['town'] = create_imput_widget('town', 'cat')
        to_predict['faculty'] = create_imput_widget('faculty', 'cat')
        to_predict['major'] = create_imput_widget('major', 'cat')
        to_predict['sch_type'] = create_imput_widget('sch_type', 'cat')
    with col3:
        to_predict['VR'] = create_imput_widget('VR','int')
        to_predict['SR'] = create_imput_widget('SR','int')
        to_predict['AR'] = create_imput_widget('AR','int')
    with col4:
        to_predict['NA'] = create_imput_widget('NA','int')
        to_predict['MR'] = create_imput_widget('MR','int')
        to_predict['CSA'] = create_imput_widget('CSA','int')


#with st.expander("Resultados de la predicción"):
model = pickle.load(open('model.pkl','rb'))

for k in to_predict.keys():
    bufer = []
    bufer.append(to_predict[k])
    to_predict[k] = bufer

df_to_predict = pd.DataFrame(to_predict)
st.dataframe(df_to_predict)

prediction = model.predict(df_to_predict)
prediction_prob = model.predict_proba(df_to_predict)
    
prediction
prediction_prob
    
    
    
    
    
    