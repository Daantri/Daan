# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import matplotlib.pyplot as plt
import altair as alt
import numpy as np
from tabulate import tabulate
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title= 'Checken')

st.title('Checken eisen en wensen')
st.write('De eisen en wensen worden momenteel gecontroleerd. Heeft u alstublieft even geduld.')
st.write('Zodra het \'Running\' icoon rechtsboven verdwenen is, kunt u verder naar de volgende pagina.')

if st.session_state.omloopplanning and st.session_state.datafile:
    st.markdown('---')
    df1 = pd.read_excel(st.session_state.datafile, engine='openpyxl')
    df2 = pd.read_excel(st.session_state.omloopplanning, engine='openpyxl')
    df3 = pd.read_excel(st.session_state.datafile,sheet_name='Afstand matrix') #deze moet aangepast

#Er moet een bus rijden op de momenten die vastgelegd zijn in de dienstregeling
    # st.header('Eis 1' )
    # st.subheader('Er moet een bus rijden op de momenten die vastgelegd zijn in de dienstregeling')
    counter_1 = 0
    lengte_df1 = len(df1['startlocatie'])
    for i in range(len(df2['startlocatie'])):
        for j in range(len(df1['startlocatie'])):
            if df1['startlocatie'][j] == df2['startlocatie'][i] and df1['eindlocatie'][j] == df2['eindlocatie'][i] and df1['vertrektijd'][j] == df2['starttijd'][i][0:5]:
                counter_1 += 1
                
            
#    if counter_1 == lengte_df1:
        #st.markdown('alle riten die gereden moeten worden, worden gereden')
#    elif counter_1 > lengte_df1:
#        minder = counter_1 - lengte_df1
        # st.markdown('de volgende ritten worden niet gereden:')
#    else:
#        meer = lengte_df1 - counter_1
        # st.markdown('de volgende ritten worden te veel gereden:')

    counter1 = abs(lengte_df1-counter_1)
    st.session_state.counter1 = counter1

    # st.header('Eis 2')
    # st.subheader('Als een bus ergens eindigt, start de bus hier weer op het moment dat hij weer gaat rijden')
#Als een bus ergens eindigt, start de bus hier weer op het moment dat hij weer gaat rijden
    counter2 = 0
    verkeerde_ritten = list()
    for k in range(len(df2['startlocatie'])-1):
        j = k + 1
        if df2['startlocatie'][j] != df2['eindlocatie'][k]:
            counter2 += 1
            verkeerde_ritten.append(df2['omloop nummer'][j])

    st.session_state.verkeerde_ritten = verkeerde_ritten
    # st.write(st.session_state.verkeerde_ritten)
            
    # if counter2 <= 0:
    #     st.markdown('alle bussen beginnen met rijden waar ze eindigen (van --> naar):')
    # else:
    #     st.markdown('de volgende ritten beginnen niet waar ze eindigen (van --> naar):')
    #     st.markdown(st.session_state.verkeerde_ritten)

    
    # st.markdown('De accucapaciteit van de bus is minimaal 10% en word niet meer opgeladen dan 90%')
    st.session_state.counter2 = counter2


    # df2['stroomgebruik']= ""
    # leegloopsnelheid = 2.2
    # idle_leegloopsnelheid = 0.01
    # oplaadsnelheid = 20
    # max_capacity_battery = 350
    
    # lijn_onder_capaciteit = []
    # lijn_boven_capaciteit = []
    # counter3 = 0
    # wenscount1 = 0
    

    # for l in range(df2['omloop nummer'].nunique()):
    #     start_percentage = st.session_state.percentage_opgeladen/100*350 #350 is de maximale State of Charge
    #     for m in range(len(df2['startlocatie'])):
            
    #         #df2['eindtijd'][m][0:1] = timedelta(minutes = )
            
    #             b = df2['starttijd'][m]
    #             e = df2['eindtijd'][m]
    #             h1,m1,s1 = b.split(':')
    #             h2,m2,s2 = e.split(':')
    #             begintijd = int(datetime.timedelta(hours=int(h1),minutes=int(m1),seconds=int(s1)).total_seconds())
    #             eindtijd = int(datetime.timedelta(hours=int(h2),minutes=int(m2),seconds=int(s2)).total_seconds())
                
    #             if b < e:
    #                 aantal_minuten = (eindtijd - begintijd)/60/60
    #             elif b > e:
    #                 eindtijd += 24*60*60
    #                 aantal_minuten = (eindtijd - begintijd)/60/60
    #             if (df2['omloop nummer'][m]==(l+1))== True:
    #                 if (df2['activiteit'][m] == 'materiaal rit')== True or (df2['activiteit'][m] == 'dienst rit')== True:
    #                     energie_verbruik = aantal_minuten * leegloopsnelheid
    #                     start_percentage += -energie_verbruik
                        
    #                 elif (df2['activiteit'][m] == 'idle') == True:
    #                     energie_verbruik = aantal_minuten * idle_leegloopsnelheid
    #                     start_percentage += -energie_verbruik
                    
    #                 elif (df2['activiteit'][m] == 'opladen') == True:
    #                     energie_verbruik = aantal_minuten * oplaadsnelheid
    #                     start_percentage += energie_verbruik
    
    #                 if (start_percentage < (0.1*max_capacity_battery))== True:
    #                     if df2['omloop nummer'][l] not in lijn_onder_capaciteit:
    #                         lijn_onder_capaciteit.append(df2['omloop nummer'][l])
    #                         counter3 += 1
    #                 elif (start_percentage > (0.9*max_capacity_battery))== True:
    #                     if df2['omloop nummer'][l] not in lijn_boven_capaciteit:
    #                         lijn_boven_capaciteit.append(df2['omloop nummer'][l])
    #                         wenscount1 += 1
    #                 df2['stroomgebruik'][m] = start_percentage
    #     st.session_state.test = df2




#De accucapaciteit van de bus is minimaal 10% en word niet meer opgeladen dan 90%
    df2['stroomgebruik'] = ""   
    leegloopsnelheid = 2.2
    idle_leegloopsnelheid = 0.01
    oplaadsnelheid = 250
    kosten_opladen = 0.37
    max_capacity_battery = st.session_state.maximumcapaciteit * st.session_state.SOH_waarde
    st.session_state.max_capacity_battery = max_capacity_battery
    lijn_onder_capaciteit = []
    lijn_boven_capaciteit = []
    counter3 = 0
    wenscount1 = 0
    st.session_state.totale_tijd = 0
    st.session_state.tijd_materiaalrit = 0
    st.session_state.totaal_kosten_opladen = 0
    

    start_percentage = []
    for l in range(df2['omloop nummer'].nunique()):
        start_capaciteit = st.session_state.percentage_opgeladen/100*max_capacity_battery #350 is de maximale State of Charge
        # st.write(st.session_state.percentage_opgeladen)
        lijst2 = []
        for m in range(len(df2['startlocatie'])):
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
            if (df2['omloop nummer'][m]==(l+1))== True:
                if (df2['activiteit'][m] == 'materiaal rit')== True:

                    
                    if (df2['startlocatie'][m] =='ehvapt' and df2['eindlocatie'][m] =='ehvbst')== True or (df2['startlocatie'][m] == 'ehvbst' and df2['eindlocatie'][m] =='ehvapt')== True:
                        energie_verbruik = df3['afstand in meters'][4]/1000* leegloopsnelheid
                        start_capaciteit += -energie_verbruik
                        st.session_state.totale_tijd += aantal_minuten
                        st.session_state.tijd_materiaalrit += aantal_minuten
                        
                        
                        st.markdown('eerste materiaal')
                        
                    
                    elif (df2['startlocatie'][m] == 'ehvbst' and df2['eindlocatie'][m] =='ehvgar')== True or (df2['startlocatie'][m] == 'ehvgar' and df2['eindlocatie'][m] == 'ehvbst') == True:
                        energie_verbruik = df3['afstand in meters'][6]/1000* leegloopsnelheid
                        start_capaciteit += -energie_verbruik
                        st.session_state.totale_tijd += aantal_minuten
                        st.session_state.tijd_materiaalrit += aantal_minuten
                        
                        st.markdown('tweede materiaal')
                    
                    elif (df2['startlocatie'][m] == 'ehvapt' and df2['eindlocatie'][m] =='ehvgar')== True or (df2['startlocatie'][m] == 'ehvgar' and df2['eindlocatie'][m] =='ehvapt') == True:
                        energie_verbruik = df3['afstand in meters'][8]/1000* leegloopsnelheid
                        start_capaciteit += -energie_verbruik
                        st.session_state.totale_tijd += aantal_minuten
                        st.session_state.tijd_materiaalrit += aantal_minuten
                        
                        st.markdown('derde materiaal')
                        

                elif (df2['activiteit'][m] == 'dienst rit')== True:

                    if (df2['startlocatie'][m] == 'ehvapt' and df2['eindlocatie'][m] == 'ehvbst') == True:
                    
                        if (df2['omloop nummer'][m] == '400'):
                            energie_verbruik = df3['afstand in meters'][0]/1000* leegloopsnelheid
                            start_capaciteit += -energie_verbruik
                            st.session_state.totale_tijd += aantal_minuten
                            
                        elif (df2['omloop nummer'][m] == '401'):
                            energie_verbruik = df3['afstand in meters'][2]/1000* leegloopsnelheid
                            start_capaciteit += -energie_verbruik
                            st.session_state.totale_tijd += aantal_minuten
                            
                    elif (df2['startlocatie'][m] == 'ehvbst' and df2['eindlocatie'][m] == 'ehvapt') == True:
                    
                        if (df2['omloop nummer'][m] == '400'):
                            energie_verbruik = df3['afstand in meters'][1]/1000* leegloopsnelheid
                            start_capaciteit += -energie_verbruik
                            st.session_state.totale_tijd += aantal_minuten
                            
                        elif (df2['omloop nummer'][m] == '401'):
                            energie_verbruik = df3['afstand in meters'][3]/1000* leegloopsnelheid
                            start_capaciteit += -energie_verbruik
                            st.session_state.totale_tijd += aantal_minuten

                  
                elif (df2['activiteit'][m] == 'idle') == True:
                    energie_verbruik = aantal_minuten * idle_leegloopsnelheid
                    start_capaciteit += -energie_verbruik
                    st.session_state.totale_tijd += aantal_minuten
                  
                elif (df2['activiteit'][m] == 'opladen') == True:
                    energie_verbruik = aantal_minuten * oplaadsnelheid
                    start_capaciteit += energie_verbruik
                    
                    if start_capaciteit > max_capacity_battery:
                        start_capaciteit = max_capacity_battery
                    st.session_state.totale_tijd += aantal_minuten
                    st.session_state.totaal_kosten_opladen += aantal_minuten * oplaadsnelheid * kosten_opladen
                    
                if (start_capaciteit < (st.session_state.minimumpercentage*max_capacity_battery))== True:
                    if df2['omloop nummer'][m] not in lijn_onder_capaciteit:
                        lijn_onder_capaciteit.append(df2['omloop nummer'][m])
                        counter3 += 1
                elif (start_capaciteit > (st.session_state.maximumpercentage*max_capacity_battery))== True:
                    if df2['omloop nummer'][m] not in lijn_boven_capaciteit:
                        lijn_boven_capaciteit.append(df2['omloop nummer'][m])
                        wenscount1 += 1
                df2['stroomgebruik'][m] = start_capaciteit
                lijst2.append(start_capaciteit/max_capacity_battery*100)
        
        start_percentage.append(lijst2)
    st.session_state.test = df2
    #st.markdown(start_percentage)
    st.session_state.lijn_boven_capaciteit = lijn_boven_capaciteit
    st.session_state.lijn_onder_capaciteit = lijn_onder_capaciteit
    #st.header('Eis 3')
    #st.subheader('Deze omloop ritten komen onder de 10% van de max capaciteit:')
    #st.markdown(st.session_state.lijn_onder_capaciteit)
    st.session_state.counter3 = counter3
        # st.write(start_percentage)
    st.session_state.laatste_accucapaciteit = []
    for i in start_percentage:
        st.session_state.laatste_accucapaciteit.append(i[-1])


    st.session_state.lijn_boven_capaciteit = lijn_boven_capaciteit
    st.session_state.lijn_onder_capaciteit = lijn_onder_capaciteit
    
    
    # st.write(start_percentage)
    st.session_state.laatste_accucapaciteit = []
    for i in start_percentage:
        st.session_state.laatste_accucapaciteit.append(i[-1])


    st.session_state.lijn_boven_capaciteit = lijn_boven_capaciteit
    st.session_state.lijn_onder_capaciteit = lijn_onder_capaciteit
    


################################################################################################################

    df2['starttijd'] = pd.to_datetime(df2['starttijd'])
    df2['eindtijd'] = pd.to_datetime(df2['eindtijd'])
    for i in range(len(df2)):
        if (str(df2['eindtijd'][i])[11:13]) < '03':
            df2['eindtijd'][i] = df2['eindtijd'].apply(lambda x: x.replace(year=2023, month=2, day=26))[i]
        else:
            df2['eindtijd'][i] = df2['eindtijd'].apply(lambda x: x.replace(year=2023, month=2, day=25))[i]
           
    for i in range(len(df2)):
        if (str(df2['starttijd'][i])[11:13]) < '03':
            df2['starttijd'][i] = df2['starttijd'].apply(lambda x: x.replace(year=2023, month=2, day=26))[i]
        else:
            df2['starttijd'][i] = df2['starttijd'].apply(lambda x: x.replace(year=2023, month=2, day=25))[i]
    
    df2.fillna('leeg', inplace=True)
    df3.fillna('leeg', inplace=True)
    df2.loc[df2['buslijn'] == " ", 'buslijn'] = 'leeg'
    # st.header('Eis 4')
    counter4 = 0
    bus_die_te_snel_rijdt = []
    for i in range(len(df2)):
        if not df2.startlocatie[i] == df2.eindlocatie[i]:
            starttijd = df2['starttijd'][i]
            beginomgezet = datetime.timedelta(hours = starttijd.hour, minutes = starttijd.minute, seconds = starttijd.second)
            eindtijd = df2['eindtijd'][i]
            eindomgezet = datetime.timedelta(hours = eindtijd.hour, minutes = eindtijd.minute, seconds = eindtijd.second)
            aantal_minuten = ((eindomgezet-beginomgezet).seconds)/60
            aantal_minuten = int(aantal_minuten)
            c = df3['min reistijd in min'].astype(int)
            if (df2.buslijn[i] == 'leeg') == True or (df2.buslijn[i] == " ") == True:
                min_reistijd = c.loc[(df3.startlocatie == df2.startlocatie[i]) & (df3.eindlocatie == df2.eindlocatie[i]) & (df3.buslijn == df2.buslijn[i]) | (df3.buslijn == " ")].values[0]
                if aantal_minuten < min_reistijd:
                    counter4 += 1
                    bus_die_te_snel_rijdt.append(df2['omloop nummer'][i])
            else:     
                min_reistijd = c.loc[(df3.startlocatie == df2.startlocatie[i]) & (df3.eindlocatie == df2.eindlocatie[i]) & (df3.buslijn == int(df2.buslijn[i]))].values[0]
                if aantal_minuten < min_reistijd:
                    counter4 += 1
                    bus_die_te_snel_rijdt.append(df2['omloop nummer'][i])
                
    # st.markdown(counter4)
    st.session_state.bus_die_te_snel_rijdt = bus_die_te_snel_rijdt
    st.session_state.counter4 = counter4
    if counter4 > 0:
        st.write('Bus(sen) ', bus_die_te_snel_rijdt, 'rijden te snel naar een route.')


    # st.header('Eis 5' )
    #Tellen hoevaak er niet op de gekozen locatie opgeladen wordt
    counter5 = 0
    a = df2.loc[(df2.activiteit == 'opladen') & (df2.startlocatie != st.session_state.garagenaam) & (df2.eindlocatie != st.session_state.garagenaam)]#ehvgar moet worden verandered naar user input
    
    counter5 += len(a)
    st.session_state.bussendienietopladenoplocatie = []
    if len(a) != 0:
        st.session_state.bussendienietopladenoplocatie = a['omloop nummer'].tolist()
    st.session_state.counter5 = counter5
    
    # st.header('Eis 6')
    #Er worden maximaal 20 bussen tegelijk opgeladen
    counter6 = 0
    if df2['omloop nummer'].nunique() > st.session_state.tegelijk_opladen:
        counter6 += 1
    
    for i in range(len(df2)):
        if (str(df2['eindtijd'][i])[11:13]) < '03':
            df2['eindtijd'][i] = df2['eindtijd'].apply(lambda x: x.replace(year=2023, month=2, day=26))[i]
        else:
            df2['eindtijd'][i] = df2['eindtijd'].apply(lambda x: x.replace(year=2023, month=2, day=25))[i]
           
    for i in range(len(df2)):
        if (str(df2['starttijd'][i])[11:13]) < '03':
            df2['starttijd'][i] = df2['starttijd'].apply(lambda x: x.replace(year=2023, month=2, day=26))[i]
        else:
            df2['starttijd'][i] = df2['starttijd'].apply(lambda x: x.replace(year=2023, month=2, day=25))[i]
    
    df2.fillna('leeg', inplace=True)
    df3.fillna('leeg', inplace=True)
    st.session_state.counter6 = counter6

    
    # st.header('Eis 7' )
    counter7 = 0
    bus_die_te_langzaam_rijdt = []
    for i in range(len(df2)):
        if not df2.startlocatie[i] == df2.eindlocatie[i]:
            starttijd = df2['starttijd'][i]
            beginomgezet = datetime.timedelta(hours = starttijd.hour, minutes = starttijd.minute, seconds = starttijd.second)
            eindtijd = df2['eindtijd'][i]
            eindomgezet = datetime.timedelta(hours = eindtijd.hour, minutes = eindtijd.minute, seconds = eindtijd.second)
            aantal_minuten = ((eindomgezet-beginomgezet).seconds)/60
            aantal_minuten = int(aantal_minuten)
            c = df3['max reistijd in min'].astype(int)
            if (df2.buslijn[i] == 'leeg') == True or (df2.buslijn[i] == " ") == True:
                max_reistijd = c.loc[(df3.startlocatie == df2.startlocatie[i]) & (df3.eindlocatie == df2.eindlocatie[i]) & (df3.buslijn == df2.buslijn[i]) | (df3.buslijn == " ")].values[0]
                if aantal_minuten > max_reistijd:
                    counter7 += 1
                    bus_die_te_langzaam_rijdt.append(df2['omloop nummer'][i])
            else:     
                max_reistijd = c.loc[(df3.startlocatie == df2.startlocatie[i]) & (df3.eindlocatie == df2.eindlocatie[i]) & (df3.buslijn == int(df2.buslijn[i]))].values[0]
                if aantal_minuten > max_reistijd:
                    counter7 += 1
                    bus_die_te_langzaam_rijdt.append(df2['omloop nummer'][i])
    # st.markdown(counter7)
    st.session_state.bus_die_te_langzaam_rijdt = bus_die_te_langzaam_rijdt
    st.session_state.counter7 = counter7
    # if counter7 > 0:
    #     st.write('Bus(sen) ', bus_die_te_langzaam_rijdt, 'rijden te langzaam naar een route.')
    #st.subheader('Eis 8' )
    DFmetBeginOplaadstation = df3[df3.startlocatie == st.session_state.garagenaam]
    dichtsbijzijnde = DFmetBeginOplaadstation['afstand in meters'].idxmin()
    dichtsbijzijnde_van_laad_station = DFmetBeginOplaadstation['eindlocatie'][dichtsbijzijnde]
    dfgefiltered = df2[(df2.startlocatie != dichtsbijzijnde_van_laad_station) & (df2.eindlocatie == st.session_state.garagenaam) & (df2.startlocatie != st.session_state.garagenaam)]
    st.session_state.busseneis8 = dfgefiltered['omloop nummer'].tolist()
    st.session_state.counter8 = len(dfgefiltered)

###### WENSEN
    # st.header('Wens 1')
    # st.subheader('Deze omloop ritten komen boven de 90% van de max capaciteit:')
    # st.markdown(st.session_state.lijn_boven_capaciteit)
    st.session_state.wenscount1 = wenscount1*st.session_state.waarde_wens1
    
    
    # st.header('Wens 2' )
    wenscount2 = 0
    minimale_oplaadtijd = st.session_state.minimale_oplaadtijd
    bussen_die_te_kort_opladen = []
    for i in range(len(df2)):
        if (df2.startlocatie[i] == df2.eindlocatie[i])==True and (df2.activiteit[i] == 'opladen')==True:
            starttijd = df2['starttijd'][i]
            beginomgezet = datetime.timedelta(hours = starttijd.hour, minutes = starttijd.minute, seconds = starttijd.second)
            eindtijd = df2['eindtijd'][i]
            eindomgezet = datetime.timedelta(hours = eindtijd.hour, minutes = eindtijd.minute, seconds = eindtijd.second)
            aantal_minuten = ((eindomgezet-beginomgezet).seconds)/60
            aantal_minuten = int(aantal_minuten)    
        if aantal_minuten < st.session_state.minimale_oplaadtijd:
            wenscount2 += 1
            bussen_die_te_kort_opladen.append(df2['omloop nummer'][i])
    # st.markdown(wenscount2)
    st.session_state.bussen_die_te_kort_opladen = bussen_die_te_kort_opladen
    st.session_state.wenscount2 = wenscount2
    # if wenscount2 > 0:
    #     st.write('Bus(sen) ', bussen_die_te_kort_opladen, 'laden te weinig minuten op')

    # st.header('Wens 3')
    st.session_state.wenscount3 = sum(df2.activiteit == 'materiaal rit')
    # st.header('Wens 4')
    st.session_state.wenscount4 = (df2['omloop nummer'].nunique())
    
pagina_4 = st.button("Volgende pagina")
if pagina_4:
    switch_page("Pagina 4 - Visueel overzicht")
