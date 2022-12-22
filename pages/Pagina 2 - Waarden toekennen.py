# -*- coding: utf-8 -*-

import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title= 'Waarden toekennen')
if st.session_state.omloopplanning and st.session_state.datafile:
    st.markdown('---')
    df1 = pd.read_excel(st.session_state.datafile, engine='openpyxl')
    df2 = pd.read_excel(st.session_state.omloopplanning, engine='openpyxl')
    df3 = pd.read_excel(st.session_state.datafile,sheet_name='Afstand matrix') #deze moet aangepast
    
st.header('Waarden toekennen')
st.write('Op deze pagina kunt u een weging toevoegen aan de verschillende wensen. Hoe hoger de waarde, hoe zwaarder de wens meeweegt.')
st.write('Kies een waarde van 0 t/m 10 en klik op Bevestig om te bevestigen.')
with st.form("Waarde toekennen aan wens 1"):
   st.write(f"Wens 1: De bussen worden tot maximaal {st.session_state.maximumpercentage*100}% opgeladen per keer")
   st.session_state.waarde_wens1 = st.slider("welke weging wilt u toekennen aan deze wens?",min_value=0, max_value=10)
   # Every form must have a submit button.
   waarde_wens1 = st.form_submit_button("Bevestig")
   if st.session_state.waarde_wens1:
       st.write("opgeslagen")

with st.form("Waarde toekennen aan wens 2"):
   st.write("Wens 2: De bussen zijn tot de benodigde hoeveelheid capaciteit van een retourrit opgeladen")
   st.session_state.waarde_wens2 = st.slider("welke weging wilt u toekennen aan deze wens?",min_value=0, max_value=10)
   waarde_wens2 = st.form_submit_button("Bevestig")
   if st.session_state.waarde_wens2:
       st.write("opgeslagen")

with st.form("Waarde toekennen aan wens 3"):
   st.write("Wens 3: De bussen rijden zo min mogelijk materiaalritten")
   st.session_state.waarde_wens3 = st.slider("welke weging wilt u toekennen aan deze wens?",min_value=0, max_value=10)
   waarde_wens3 = st.form_submit_button("Bevestig")
   if st.session_state.waarde_wens3:
       st.write("opgeslagen")

with st.form("Waarde toekennen aan wens 4"):
   st.write("Wens 4: Het aantal bussen is minimaal")
   st.session_state.waarde_wens4 = st.slider("welke weging wilt u toekennen aan deze wens?",min_value=0, max_value=10)
   waarde_wens4 = st.form_submit_button("Bevestig")
   if st.session_state.waarde_wens4:
       st.write("opgeslagen")

pagina_3 = st.button("Volgende pagina")
if pagina_3:
    switch_page("Pagina 3 - Checken")
