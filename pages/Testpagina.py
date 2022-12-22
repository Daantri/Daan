# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd

df2 = pd.read_excel('C:/Users/amber/OneDrive - Office 365 Fontys/Fontys/LEERJAAR 2/Project 6/Week 2/Omloop planning.xlsx')
df1 = pd.read_excel('C:/Users/amber/OneDrive - Office 365 Fontys/Fontys/LEERJAAR 2/Project 6/Week 2/Connexxion data - 2022-2023.xlsx') 


leegloopsnelheid = 2.2
idle_leegloopsnelheid = 0.01
oplaadsnelheid = 20
max_capacity_battery = 350
minimumpercentage = 0.1
maximumpercentage = 0.9
lijn_onder_capaciteit = []
lijn_boven_capaciteit = []
counter3 = 0
wenscount1 = 0

for l in range(df2['omloop nummer'].nunique()):
    start_percentage = st.session_state.percentage_opgeladen/100*st.session_state.maximumcapaciteit #350 is de maximale State of Charge
    for m in range(len(df2['startlocatie'])):
        #df2['eindtijd'][m][0:1] = timedelta(minutes = )
        
            b = df2['starttijd'][m]
            e = df2['eindtijd'][m]
            h1,m1,s1 = b.split(':')
            h2,m2,s2 = e.split(':')
            begintijd = int(datetime.timedelta(hours=int(h1),minutes=int(m1),seconds=int(s1)).total_seconds())
            eindtijd = int(datetime.timedelta(hours=int(h2),minutes=int(m2),seconds=int(s2)).total_seconds())
            
            if b < e:
                aantal_minuten = (eindtijd - begintijd)/60/60
            elif b > e:
                eindtijd += 24*60*60
                aantal_minuten = (eindtijd - begintijd)/60/60
            
            if (df2['activiteit'][m] == 'materiaal rit')== True or (df2['activiteit'][m] == 'dienst rit')== True:
                energie_verbruik = aantal_minuten * leegloopsnelheid
                start_percentage += -energie_verbruik
                
            elif (df2['activiteit'][m] == 'idle') == True:
                    energie_verbruik = aantal_minuten * idle_leegloopsnelheid
                    start_percentage += -energie_verbruik
            
            elif (df2['activiteit'][m] == 'opladen') == True:
                    energie_verbruik = aantal_minuten * oplaadsnelheid
                    start_percentage += energie_verbruik

            if (start_percentage < (minimumpercentage*max_capacity_battery))== True:
                if df2['omloop nummer'][l] not in lijn_onder_capaciteit:
                    lijn_onder_capaciteit.append(df2['omloop nummer'][l])
                    counter3 += 1
            elif (start_percentage > (maximumpercentage*max_capacity_battery))== True:
                if df2['omloop nummer'][l] not in lijn_boven_capaciteit:
                    lijn_boven_capaciteit.append(df2['omloop nummer'][l])
                    wenscount1 += 1
            percentage = start_percentage /350*100 # dit is het percentage van de bus
            st.markdown(percentage)



