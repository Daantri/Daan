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
    page_title= "Samenvatting")
st.title("Samenvatting")
# st.dataframe({
#         "omloop nummer van de bus < 10% ": [lijn_onder_capaciteit],
#         "omloop nummer van de bus > 90%": [lijn_boven_capaciteit],})

        
#st.checkbox("Use container width", value=False, key="use_container_width")
data = {"Eisen": ["Eis 1: Bussen die niet rijden op de momenten die vastgelegd zijn",
                  "Eis 2: Bussen beginnen niet waar ze eindigen", 
                  f"Eis 3: Bussen met een accucapaciteit niet lager dan {st.session_state.minimumpercentage*100}%", 
                  "Eis 4: Bussen die niet op de gekozen locatie opgeladen worden",
                  f"Eis 5: Niet meer dan {st.session_state.tegelijk_opladen} bussen laden tegelijk op",
                  "Eis 6: Bussen rijden niet te snel van locatie naar locatie",
                  "Eis 7: Bussen rijden niet te langzaam van locatie naar locatie",
                 "Eis 8: Bussen rijden alleen van het dichstbijzijnde station naar oplaadstation"]}
# "Omloop nummer":[st.session_state.counter1,
#   st.session_state.verkeerde_ritten,
#   st.session_state.lijn_onder_capaciteit,
#   st.session_state.bussendienietopladenoplocatie,
#   st.session_state.bus_die_te_snel_rijdt,
#   st.session_state.bus_die_te_langzaam_rijdt
#   ]}

                        
data2 = pd.DataFrame(data)
data2['Omloop nummer'] = ''
data2.at[0, 'Omloop nummer']= st.session_state.counter1
data2.at[1, 'Omloop nummer']= st.session_state.verkeerde_ritten
data2.at[2, 'Omloop nummer']= st.session_state.lijn_onder_capaciteit
data2.at[3, 'Omloop nummer']= st.session_state.bussendienietopladenoplocatie
data2.at[4, 'Omloop nummer']= st.session_state.counter6
data2.at[5, 'Omloop nummer']= st.session_state.bus_die_te_snel_rijdt
data2.at[6, 'Omloop nummer']= st.session_state.bus_die_te_langzaam_rijdt
data2.at[7, 'Omloop nummer']= st.session_state.busseneis8
data2['Omloop nummer']=data2['Omloop nummer'].astype('str')
a = []
data2.loc[data2['Omloop nummer']=='0' ,'Omloop nummer']="Voldoet"
data2.loc[data2['Omloop nummer']=='[]' ,'Omloop nummer']="Voldoet"
# data2.loc[,'Omloop nummer']="n.v.t."
if len(st.session_state.lijn_boven_capaciteit)

st.dataframe(data2)
data3 = {
        "Wensen": [f"Wens 1: De bussen worden tot maximaal {st.session_state.maximumpercentage*100}% opgeladen per keer",
                  "Wens 2: De bussen zijn tot de benodigde hoeveelheid capaciteit van een retourrit opgeladen", 
                  "Wens 3: De bussen rijden zo min mogelijk materiaalritten", 
                  "Wens 4: Het aantal bussen is minimaal"]}
data4 = pd.DataFrame(data3)
data4['Wensovertreding'] = ''
data4.at[0, 'Wensovertreding'] = st.session_state.wenscount1
data4.at[1, 'Wensovertreding'] = st.session_state.bussen_die_te_kort_opladen
data4.at[2, 'Wensovertreding'] = st.session_state.lijn_boven_capaciteit
data4.at[3, 'Wensovertreding'] = f"{st.session_state.wenscount4} aantal bussen"
                        
pagina_6 = st.button("Volgende pagina")
if pagina_6:
    switch_page("Pagina 6 - Gantt-diagram en lijngrafiek") 
