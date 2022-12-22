# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import matplotlib.pyplot as plt
import altair as alt
import numpy as np

st.subheader('Beschrijving van de Eisen')

if st.session_state.counter1 > 0:
    st.markdown('beschrijving Eis 1')
    st.text_area('Eis 1', '''Eis 1 was gemaakt om te checken of er inderdaad 
    een bus rijdt op de momenten die vastgelegd zijn in de 
    dienstregeling.
    De rede dat er niet aan Eis 1 wordt voldaan is omdat er ............''')
    
if st.session_state.counter2 > 0:
    st.markdown('beschrijving Eis 2')
    st.text_area('Eis 2', '''.....................''')
    
    
if st.session_state.counter3 > 0:
    st.markdown('beschrijving Eis 3')
    st.text_area('Eis 3', '''.....................''')
    
if st.session_state.counter4 > 0:
    st.markdown('beschrijving Eis 4')
    st.text_area('Eis 4', '''.....................''')
    
if st.session_state.counter5 > 0:
    st.markdown('beschrijving Eis 5')
    st.text_area('Eis 5', '''.....................''')

if st.session_state.counter6 > 0:
    st.markdown('beschrijving Eis 6')
    st.text_area('Eis 6', '''.....................''')
    
if st.session_state.counter7 > 0:
    st.markdown('beschrijving Eis 7')
    st.text_area('Eis 7', '''.....................''')

