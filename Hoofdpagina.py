# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 10:03:56 2022

@author: amber
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle as pkle
import os.path
from datetime import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page



st.set_page_config(
    page_title = "Tool checken omloopplanning",
)

st.title('Uploaden data')
st.markdown('Upload de data als het aangegeven format in de handleiding.')


col1, col2 = st.columns(2)


with col1:
    st.session_state.omloopplanning = st.file_uploader('Kies het bestand met de omloopplanning', type= 'xlsx')
with col2:
    st.session_state.datafile = st.file_uploader('Kies het bestand met de data', type= 'xlsx')


keuzes = {'Upload eerst de bovenstaande bestanden'}

if st.session_state.omloopplanning and st.session_state.datafile:
    st.markdown('---')
    df1 = pd.read_excel(st.session_state.datafile, engine='openpyxl')
    df2 = pd.read_excel(st.session_state.omloopplanning, engine='openpyxl')
    df3 = pd.read_excel(st.session_state.datafile,sheet_name='Afstand matrix') #deze moet aangepast
    keuzes = sorted(set(df2['startlocatie']))
    

radio = st.radio(
    "Hoe wordt het oplaadstation genoemd?",
    keuzes,
)
st.session_state.garagenaam = radio


pagina_1 = st.button("Volgende pagina")
if pagina_1:
    switch_page("Pagina 1 - Vaste startwaarden")
# if st.session_state.omloopplanning:
#     df = pd.read_excel(st.session_state.omloopplanning)
#     st.dataframe(df)

# if st.session_state.tweede:
#     df = pd.read_excel(st.session_state.tweede)
#     st.dataframe(df)

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

show_pdf('Explanation tool.pdf')
