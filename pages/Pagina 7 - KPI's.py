# -- coding: utf-8 --
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import matplotlib.pyplot as plt
import altair as alt
import numpy as np
from tabulate import tabulate

st.set_page_config(
    page_title= 'KPI\'s')

st.title('KPI\'s')
if st.session_state.omloopplanning and st.session_state.datafile:
    st.markdown('---')
    df1 = pd.read_excel(st.session_state.datafile, engine='openpyxl')
    df2 = pd.read_excel(st.session_state.omloopplanning, engine='openpyxl')
    df3 = pd.read_excel(st.session_state.datafile,sheet_name='Afstand matrix') #deze moet aangepast
    counter_dienst = df2['activiteit'].value_counts()['dienst rit']
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Totaal aantal benodigde bussen:')
        aantal_bussen = df2['omloop nummer'].nunique()
        st.header(aantal_bussen)
        
        st.subheader('Percentage aantal gemaakte materiaalritten t.a.v. alle gemaakte ritten:')
        counter_materiaal = df2['activiteit'].value_counts()['materiaal rit']
        per_materiaal_rit = (counter_materiaal/(counter_materiaal+counter_dienst))*100
        st.header(f'{int(per_materiaal_rit)}%')

##########################################################################################
    with col2:
        st.subheader('Totaal aantal gemaakte materiaal ritten:')
        counter_materiaal = df2['activiteit'].value_counts()['materiaal rit']
        st.header(counter_materiaal)

        st.subheader('Percentage gemaakte materiaalritten t.a.v. totale tijd:')
        tijd = (st.session_state.tijd_materiaalrit /st.session_state.totale_tijd)*100
        st.header(f'{int(tijd)}%')
###########################################################################################



#########################################################################################
    with col1: 
        oplaadsnelheid = 250
        kosten_opladen = 0.37
        max_capacity_battery = st.session_state.maximumcapaciteit * st.session_state.SOH_waarde
    
        kosten_bijladen = 0  # NIEUW
        st.markdown(max_capacity_battery)
        for i in st.session_state.laatste_accucapaciteit:
            ii = i/100*max_capacity_battery
            if ii < max_capacity_battery*(st.session_state.percentage_opgeladen/100):
                kosten_bijladen += (max_capacity_battery - ii)/oplaadsnelheid * kosten_opladen
        st.subheader('kosten voor het opladen in de gemaakte planning:')
        st.subheader(f'€{int(st.session_state.totaal_kosten_opladen)}')
    
    with col2:
        st.subheader('kosten voor het extra bijladen aan het einde van de planning (terug naar de start waarde)')
        st.subheader(f'€{int(kosten_bijladen)}')
        
        
##################################################################################
    with col1: 
        terug_aan_net = 0

        for i in st.session_state.laatste_accucapaciteit:
            ii = i/100*max_capacity_battery
            if ii > max_capacity_battery*(st.session_state.percentage_opgeladen/100):      # de 350 moet vervangen worden door de juiste st.sessions_state..............
                terug_aan_net += abs(((max_capacity_battery*st.session_state.percentage_opgeladen/100) - ii))

        if terug_aan_net > 0:
            st.subheader('Hoeveel Kwh kan er aan het einde van de dag worden terug gegeven aan het net:')
            st.header(f'{int(terug_aan_net)} kWh')
