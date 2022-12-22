# -*- coding: utf-8 -*-

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.chart_container import chart_container

st.set_page_config(
    page_title= 'Gantt-diagram en lijngrafiek')



    
st.title('Gantt-diagram en lijngrafiek')
st.markdown('Beide grafieken zijn als PNG te downloaden door de cursor op de grafiek te houden en op het cameraatje bovenin te klikken.')
st.header('Gantt-diagram')
df3 = st.session_state.test
st.write('De legenda is op volgorde van **grootte**. Dat wil dus zeggen dat het onderdeel waar het meeste tijd in zit, bovenaan staat.')

planning = pd.read_excel(st.session_state.omloopplanning)
dienstregeling = pd.read_excel(st.session_state.datafile, sheet_name='Dienstregeling')
afstand_matrix = pd.read_excel(st.session_state.datafile, sheet_name='Afstand matrix')
#pd.read_excel(r'C:/Users/amber/OneDrive - Office 365 Fontys/Fontys/LEERJAAR 2/Project 6/Week 2/nieuwe map/Omloop planning.xlsx')

#data = pd.read_excel(r'C:\Users\daanr\Documents\TW jaar 2\Project\Project 6\streamlit\Omloopplanning.xlsx')
omloopplanning = df3[["omloop nummer", "starttijd", "eindtijd", "activiteit", "buslijn", "stroomgebruik"]]

omloopplanning['starttijd'] = pd.to_datetime(omloopplanning['starttijd'])
omloopplanning['eindtijd'] = pd.to_datetime(omloopplanning['eindtijd'])

for i in range(len(omloopplanning)):
    if (omloopplanning["buslijn"][i])!= 'leeg':
        omloopplanning["activiteit"][i] = omloopplanning["buslijn"][i]

for i in range(len(omloopplanning)):
    if not omloopplanning["activiteit"][i] == 'materiaal rit':
        if not omloopplanning["activiteit"][i] == 'opladen':
            if not omloopplanning["activiteit"][i] == 'idle':
                omloopplanning["activiteit"][i] = 'Buslijn ' + str(int(omloopplanning["activiteit"][i]))
                
for i in range(len(omloopplanning)):
    if (str(omloopplanning['eindtijd'][i])[11:13]) < '03':
        omloopplanning['eindtijd'][i] = omloopplanning['eindtijd'].apply(lambda x: x.replace(year=2023, month=2, day=26))[i]
    else:
       omloopplanning['eindtijd'][i] = omloopplanning['eindtijd'].apply(lambda x: x.replace(year=2023, month=2, day=25))[i]
       
for i in range(len(omloopplanning)):
    if (str(omloopplanning['starttijd'][i])[11:13]) < '03':
        omloopplanning['starttijd'][i] = omloopplanning['starttijd'].apply(lambda x: x.replace(year=2023, month=2, day=26))[i]
    else:
        omloopplanning['starttijd'][i] = omloopplanning['starttijd'].apply(lambda x: x.replace(year=2023, month=2, day=25))[i]




fig = px.timeline(omloopplanning, x_start="starttijd", x_end="eindtijd", y="omloop nummer", color="activiteit")
fig.update_yaxes(autorange="reversed")
st.plotly_chart(fig)
#st.dataframe(omloopplanning)
st.header('Verloop accucapaciteit (in kWh)')
fig2 = px.line(omloopplanning, x="starttijd", y="stroomgebruik", color='omloop nummer')
st.plotly_chart(fig2)

pagina_7 = st.button("Volgende pagina")
if pagina_7:
    switch_page("Pagina 7 - KPI's")
