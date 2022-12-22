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
    page_title= 'Samenvatting')
st.title('Samenvatting')
# st.dataframe({
#         "omloop nummer van de bus < 10% ": [lijn_onder_capaciteit],
#         "omloop nummer van de bus > 90%": [lijn_boven_capaciteit],})

#st.checkbox("Use container width", value=False, key="use_container_width")
st.dataframe({
        "Eisen": ['Eis 1:Bussen die niet rijden op de momenten die vastgelegd zijn',
                  'Eis 2: Bussen beginnen niet waar ze eindigen', 
                  'Eis 3: Bussen met een accucapaciteit <10%', 
                  'Eis 4: Bussen met een accucapaciteit >90%',
                  'Eis 5 Bussen die niet op de gekozen locatie opgeladen worden',
                  'Eis 6: ',
                  'Eis 7: ',
                  'Eis 8:',
                  'Eis 9:'],
        "Omloop nummer": ['in te vullen eis 1*******',
                            st.session_state.verkeerde_ritten,
                          st.session_state.lijn_onder_capaciteit,
                          st.session_state.lijn_boven_capaciteit,
                          'in te vullen eis 5*******',
                          'in te vullen eis 6*******',
                          st.session_state.bus_die_te_snel_rijdt,
                          st.session_state.bus_die_te_langzaam_rijdt,
                          st.session_state.bussen_die_te_kort_opladen]})
pagina_6 = st.button("Volgende pagina")
if pagina_6:
    switch_page("Pagina 6 - Gantt-diagram en lijngrafiek") 
