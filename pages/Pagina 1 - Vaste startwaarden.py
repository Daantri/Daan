# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import matplotlib.pyplot as plt
import altair as alt
import numpy as np
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title= 'Vaste startwaarden')

if st.session_state.omloopplanning and st.session_state.datafile:
    st.markdown('---')
    df1 = pd.read_excel(st.session_state.datafile, engine='openpyxl')
    df2 = pd.read_excel(st.session_state.omloopplanning, engine='openpyxl')
    df3 = pd.read_excel(st.session_state.datafile,sheet_name='Afstand matrix') #deze moet aangepast
     


st.write('Deze waarden zijn aanbevolen om te gebruiken, maar kunnen nu ook aangepast worden.')
maximumcapaciteit = st.number_input('Wat is de **maximumcapaciteit** van de bus (in kWh)?', value =350)
st.session_state.maximumcapaciteit = maximumcapaciteit

minimumpercentage = st.number_input("Wat is de **minimumpercentage** van de bus (in %)? Dus onder welk percentage mag de bus niet komen?", value =10)
st.session_state.minimumpercentage = minimumpercentage/100

maximumpercentage = st.number_input('Wat is het **maximumpercentage** van de bus (in %)? Dus tot welk percentage kan de bus zo optimaal mogelijk opladen?', value =90)
st.session_state.maximumpercentage = maximumpercentage/100

minimale_oplaadtijd = st.number_input('Wat is de **minimale oplaadtijd** van de bus (in minuten)? Dus hoe lang moet een bus minimaal kunnen opladen?', value =15)
st.session_state.minimale_oplaadtijd = minimale_oplaadtijd

SOH_waarde = st.number_input('Wat is de **SOH-waarde** van de bus (in %)? Dus welk percentage van de originele capaciteit heeft de bus nog?', value =85)
st.session_state.SOH_waarde = SOH_waarde/100

tegelijk_opladen = st.number_input('Wat is het **aantal bussen** dat tegelijkertijd kan **opladen**?', value =20)
st.session_state.tegelijk_opladen = tegelijk_opladen

#col1, = st.columns(1)
with st.form("Capaciteit bus"):
   st.write("Tot hoeveel procent zijn de accus bij aanvang van de dienst opgeladen?")
   st.session_state.percentage_opgeladen = st.slider('capaciteit bussen (in %)', value=80)
   percentage_opgeladen = st.form_submit_button("Submit")
   if st.session_state.percentage_opgeladen:
       st.write("opgeslagen")

pagina_2 = st.button("Volgende pagina")
if pagina_2:
    switch_page("Pagina 2 - Waarden toekennen")
