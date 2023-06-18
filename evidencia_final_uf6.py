import streamlit as st
import numpy as np
import pandas as pd
import plotly as px
import plotly.figure_factory as ff
from bokeh.plotting import figure
import matplotlib.pyplot as plt
from PIL import Image

st.title('Police Incidents Reports from 2018 to 2020 in San Francisco')
st.markdown('Evidencia Natalia Ovando Flores A01368118 :sunglasses:') # modificacion 1
image = Image.open('sdpd logo.png')
st.image(image, use_column_width=True, width=50, caption='San Francisco Police Department Logo') # modificacion 2
df = pd.read_csv('Police_Department_Incident_Reports__2018_to_Present.csv')
st.dataframe(df)
st.markdown('The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution.')

mapa = pd.DataFrame()
mapa['Date']= df['Incident Date']
mapa['Day']= df['Incident Day of Week']
mapa['Police District']= df['Police District']
mapa['Neighborhood']= df['Analysis Neighborhood']
mapa['Incident Category']= df['Incident Subcategory']
mapa['Resolution'] = df['Resolution'] # columma agregada
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa['Incident Code'] = df['Incident Code'] # columma agregada
mapa['Incident Subcategory']=df['Incident Subcategory'] # columma agregada
mapa['Incident Year']=df['Incident Year'] # columma agregada
mapa = mapa.dropna()
#st.map(mapa.astype({'lat': 'float32', 'lon': 'float32'}))

subset_data2=mapa
police_district_input= st.sidebar.multiselect(
    'Police District',
    mapa.groupby('Police District').count().reset_index()['Police District'].tolist())
if len(police_district_input)>0:
    subset_data2=mapa[mapa['Police District'].isin(police_district_input)]
    

subset_data1=subset_data2
neighborhood_input= st.sidebar.multiselect(
    'Neighborhood',
    mapa.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist())
if len(neighborhood_input)>0:
    subset_data1=subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]


subset_data=subset_data1
incident_input= st.sidebar.multiselect(
    'Incident Category',
    mapa.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
if len(incident_input)>0:
    subset_data=subset_data1[subset_data1['Incident Category'].isin(incident_input)]
    
subset_data

st.markdown('It is important to mention that any police district can answer to any incident, the neighborhood in which it happened is not related to the police district.')
st.markdown('Crime locations in San Francisco')
st.map(subset_data)
st.markdown('Crimes ocurred per day of the week')
st.bar_chart(subset_data['Day'].value_counts())
st.markdown('Crimes ocurred per date')
st.line_chart(subset_data['Date'].value_counts())

col1, col2 = st.columns(2) # modificacion 3
with col1:
    st.markdown('Types of crimes commited')
    st.bar_chart(subset_data['Incident Category'].value_counts())
with col2:
    st.markdown('Crimes per Year')
    st.bar_chart(subset_data['Incident Year'].value_counts()) # modificacion 4 nueva grafica

st.markdown('Distribution of Report Type') # modificacion 5 nueva grafica
fig2, ax1= plt.subplots()
labels=df['Report Type Description'].unique()
ax1.pie(df['Report Type Description'].value_counts(), labels=labels, autopct='%1.1f%%',startangle=20)
st.pyplot(fig2)

agree = st.button('Click to see Incident Subcategories &#x2193;') # modificacion 6 se agrego emoji
if agree:
    st.markdown('Subtype of crimes commited')
    st.bar_chart(subset_data['Incident Subcategory'].value_counts())
    
    
st.markdown('Resolution Status')
fig1, ax1= plt.subplots()
labels=subset_data['Resolution'].unique()
ax1.pie(subset_data['Resolution'].value_counts(), labels=labels, autopct='%1.1f%%',startangle=20)
st.pyplot(fig1)

st.markdown('Report Type Distribution') # modificacion 7 nueva grafica
st.bar_chart(subset_data['Incident Code'].value_counts())

