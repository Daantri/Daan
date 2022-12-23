# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import matplotlib.pyplot as plt
import altair as alt
import numpy as np
import plotly.graph_objects as go
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title= 'Visueel overzicht')
# col1, col2 = st.columns(2)
st.write(st.session_state.counter1, st.session_state.counter2, st.session_state.counter3, st.session_state.counter4, st.session_state.counter5, st.session_state.counter6, st.session_state.counter7, st.session_state.counter8)
opgeteld = st.session_state.counter1 + st.session_state.counter2 + st.session_state.counter3 + st.session_state.counter4 + st.session_state.counter5 + st.session_state.counter6 + st.session_state.counter7 + st.session_state.counter8
# with col1:
if opgeteld == 0:
    st.markdown('De planning voldoet aan alle eisen.')
else:
    st.markdown('De planning voldoet niet aan alle eisen. In de diagram hieronder is te zien welke eisen de grootste penalty\'s hebben')
    st.header('Pie chart Eisen')
    labels_eisen = 'Eis 1', 'Eis 2', 'Eis 3','Eis 4','Eis 5','Eis 6','Eis 7', 'Eis 8',
    sizes_eisen = [st.session_state.counter1, 
                   st.session_state.counter2, 
                   st.session_state.counter3, 
                   st.session_state.counter4, 
                   st.session_state.counter5, 
                   st.session_state.counter6, 
                   st.session_state.counter7, 
                   st.session_state.counter8]

    

    # fig1, ax1 = plt.subplots()
    # ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
    #     shadow=True, startangle=90)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
    
    # fig_eisen = go.Figure(data=[go.Pie(labels=labels_eisen, values=sizes_eisen)])
    # fig_eisen.update_traces(hoverinfo='label+percent', textinfo='value', textposition='inside', textfont_size=20,marker=dict(colors=colors, line=dict(color='#000000', width=2)))
fig_eisen = px.pie(values=sizes_eisen, names = labels_eisen, title = 'Eisen')
fig_eisen.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
fig_eisen.update_traces(hoverinfo='label+percent', textinfo='value', textposition='inside', textfont_size=12)
st.plotly_chart(fig_eisen)
    # fig_eisen.show()
    
# with col2:
    ############################# FICTIEVE WAARDE
counter1w = st.session_state.wenscount1*st.session_state.waarde_wens1
counter2w = st.session_state.wenscount2*st.session_state.waarde_wens2
counter3w = st.session_state.wenscount3*st.session_state.waarde_wens3
counter4w = st.session_state.wenscount4*st.session_state.waarde_wens4

#############################

# Pie chart Wensen met totaal aantal counters
st.header('Pie chart Wensen')
if st.session_state.waarde_wens1==0 and st.session_state.waarde_wens2==0 and st.session_state.waarde_wens3==0 and st.session_state.waarde_wens4 == 0:
    st.write('Zorg dat je de wegingen ingevuld hebt op Pagina 2: Waarden toekennen!')
else:
    st.write('Komt hier nu geen plot te staan? Dan wil dat zeggen dat er aan alle wensen **mét** toegekende waarden, voldaan wordt.')
    labels_wensen = 'Wens 1', 'Wens 2', 'Wens 3', 'Wens 4'
    sizes_wensen = [counter1w, counter2w, counter3w, counter4w]
    
    fig_wensen = px.pie(values=sizes_wensen, names = labels_wensen, title = 'Wensen')
    fig_wensen.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    fig_wensen.update_traces(hoverinfo='label+percent', textinfo='value', textposition='inside', textfont_size=12)
    st.plotly_chart(fig_wensen)

st.write(f'Weging wens 1: {st.session_state.waarde_wens1}')
st.write(f'Weging wens 2: {st.session_state.waarde_wens2}')
st.write(f'Weging wens 3: {st.session_state.waarde_wens3}')
st.write(f'Weging wens 4: {st.session_state.waarde_wens4}')

pagina_5 = st.button("Volgende pagina")
terug_naar_2 = st.button("Terug naar Pagina 2")
if pagina_5:
    switch_page("Pagina 5 - Samenvatting")
if terug_naar_2:
    switch_page("Pagina 2 - Waarden toekennen")
