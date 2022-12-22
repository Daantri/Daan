# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import matplotlib.pyplot as plt
import altair as alt
import numpy as np

st.set_page_config(
    page_title= 'EISEN')

st.title('Eisen')




st.sidebar.success('select a page above2.')


if st.session_state.upload_first_file and st.session_state.upload_second_file:
    st.markdown('---')
    df1 = pd.read_excel(st.session_state.upload_first_file, engine='openpyxl')
    df2 = pd.read_excel(st.session_state.upload_second_file, engine='openpyxl')
    df3 = pd.read_excel(st.session_state.upload_first_file,sheet_name='Afstand matrix') #deze moet aangepast



#Er moet een bus rijden op de momenten die vastgelegd zijn in de dienstregeling
    st.subheader('Eis 1' )
    st.markdown('Er moet een bus rijden op de momenten die vastgelegd zijn in de dienstregeling')
    counter_1 = 0
    lengte_df1 = len(df1['startlocatie'])
    for i in range(len(df2['startlocatie'])):
        for j in range(len(df1['startlocatie'])):
            if df1['startlocatie'][j] == df2['startlocatie'][i] and df1['eindlocatie'][j] == df2['eindlocatie'][i] and df1['vertrektijd'][j] == df2['starttijd'][i][0:5]:
                counter_1 += 1
                
            
    if counter_1 == lengte_df1:
        st.markdown('alle riten die gereden moeten worden, worden gereden')
    elif counter_1 > lengte_df1:
        minder = counter_1 - lengte_df1
        st.markdown('de volgende ritten worden niet gereden:')
    else:
        meer = lengte_df1 - counter_1
        st.markdown('de volgende ritten worden te veel gereden:')

    counter1 = abs(lengte_df1-counter_1)


    st.subheader('Eis 2')
    st.markdown('Als een bus ergens eindigt, start de bus hier weer op het moment dat hij weer gaat rijden')
#Als een bus ergens eindigt, start de bus hier weer op het moment dat hij weer gaat rijden
    counter2 = 0
    verkeerde_ritten = []
    for k in range(len(df2['startlocatie'])-1):
        j = k + 1
        if df2['startlocatie'][j] != df2['eindlocatie'][k]:
            counter2 += 1
            verkeerde_ritten.append(df2['startlocatie'], df2['eindlocatie'][k], df2['omloop nummer'][j])
            
    if counter2 <= 0:
        st.markdown('alle bussen beginnen met rijden waar ze eindigen (van --> naar):')
    else:
        st.markdown('de volgende ritten beginnen niet waar ze eindigen (van --> naar):')
        st.markdown(verkeerde_ritten)




    
    st.markdown('De accucapaciteit van de bus is minimaal 10% en word niet meer opgeladen dan 90%')
#De accucapaciteit van de bus is minimaal 10% en word niet meer opgeladen dan 90%
    leegloopsnelheid = 2.2
    idle_leegloopsnelheid = 0.01
    oplaadsnelheid = 20
    max_capacity_battery = 350
    
    lijn_onder_capaciteit = []
    lijn_boven_capaciteit = []
    counter3 = 0
    counter4 = 0
    
    
    
    
    
    
    
    for l in range(df2['omloop nummer'].nunique()):
        start_percentage = st.session_state.percentage_opgeladen/100*350 #350 is de maximale State of Charge
        omloopnummer = []
        omloopnummer.append(df2['omloop nummer'][l])
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

                if (start_percentage < (0.1*max_capacity_battery))== True:
                    if df2['omloop nummer'][l] not in lijn_onder_capaciteit:
                        lijn_onder_capaciteit.append(df2['omloop nummer'][l])
                        counter3 += 1
                elif (start_percentage > (0.9*max_capacity_battery))== True:
                    if df2['omloop nummer'][l] not in lijn_boven_capaciteit:
                        lijn_boven_capaciteit.append(df2['omloop nummer'][l])
                        counter4 += 1


    st.subheader('Eis 3')
    st.markdown('Deze omloop ritten komen onder de 10% van de max capaciteit:')
    st.markdown(lijn_onder_capaciteit)
    
    st.subheader('Eis 4')
    st.markdown('Deze omloop ritten komen boven de 90% van de max capaciteit:')
    st.markdown(lijn_boven_capaciteit)


################################################################################################################

    df2['starttijd'] = pd.to_datetime(df2['starttijd'])
    df2['eindtijd'] = pd.to_datetime(df2['eindtijd'])

    st.subheader('Eis 5' )
    #Tellen hoevaak er niet op de gekozen locatie opgeladen wordt
    counter5 = 0
    a = df2.loc[(df2.activiteit == 'opladen') & (df2.startlocatie != 'ehvgar') & (df2.eindlocatie != 'ehvgar')]#ehvgar moet worden verandered naar user input
    counter5 += len(a)
    
    st.markdown('Eis 6')
    #Er worden maximaal 20 bussen tegelijk opgeladen
    counter6 = 0
    if df2['omloop nummer'].nunique() > 20:
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
    
    st.subheader('Eis 7' )
    counter7 = 0
    for i in range(len(df2)):
        if not df2.startlocatie[i] == df2.eindlocatie[i]:
            starttijd = df2['starttijd'][i]
            beginomgezet = datetime.timedelta(hours = starttijd.hour, minutes = starttijd.minute, seconds = starttijd.second)
            eindtijd = df2['eindtijd'][i]
            eindomgezet = datetime.timedelta(hours = eindtijd.hour, minutes = eindtijd.minute, seconds = eindtijd.second)
            aantal_minuten = ((eindomgezet-beginomgezet).seconds)/60
            aantal_minuten = int(aantal_minuten)
            c = df3['min reistijd in min'].astype(int)
            min_reistijd = c.loc[(df3.startlocatie == df2.startlocatie[i]) & (df3.eindlocatie == df2.eindlocatie[i]) & (df3.buslijn == df2.buslijn[i])].values[0]
            if aantal_minuten < min_reistijd:
                counter7 += 1
                
    st.markdown(counter5)
    
    st.subheader('Eis 8' )
    counter8 = 0
    for i in range(len(df2)):
        if not df2.startlocatie[i] == df2.eindlocatie[i]:
            starttijd = df2['starttijd'][i]
            beginomgezet = datetime.timedelta(hours = starttijd.hour, minutes = starttijd.minute, seconds = starttijd.second)
            eindtijd = df2['eindtijd'][i]
            eindomgezet = datetime.timedelta(hours = eindtijd.hour, minutes = eindtijd.minute, seconds = eindtijd.second)
            aantal_minuten = ((eindomgezet-beginomgezet).seconds)/60
            aantal_minuten = int(aantal_minuten)
            c = df3['max reistijd in min'].astype(int)
            min_reistijd = c.loc[(df3.startlocatie == df2.startlocatie[i]) & (df3.eindlocatie == df2.eindlocatie[i]) & (df3.buslijn == df2.buslijn[i])].values[0]
            if aantal_minuten > min_reistijd:
                counter6 += 1
    st.markdown(counter6)
    
    
    st.subheader('Eis 9' )
    counter9 = 0
    minimaale_oplaadtijd = 15
    for i in range(len(df2)):
        if (df2.startlocatie[i] == df2.eindlocatie[i])==True and (df2.activiteit[i] == 'opladen')==True:
            starttijd = df2['starttijd'][i]
            beginomgezet = datetime.timedelta(hours = starttijd.hour, minutes = starttijd.minute, seconds = starttijd.second)
            eindtijd = df2['eindtijd'][i]
            eindomgezet = datetime.timedelta(hours = eindtijd.hour, minutes = eindtijd.minute, seconds = eindtijd.second)
            aantal_minuten = ((eindomgezet-beginomgezet).seconds)/60
            aantal_minuten = int(aantal_minuten)    
        if aantal_minuten < minimaale_oplaadtijd:
            counter9 += 1
    st.markdown(counter9)
    
    
    ########################################################################### FIGUREN EN TABELLEN
    ##############################################################################################
    
    
    st.subheader('Samenvatting')
    # st.dataframe({
    #         "omloop nummer van de bus < 10% ": [lijn_onder_capaciteit],
    #         "omloop nummer van de bus > 90%": [lijn_boven_capaciteit],})
    
    st.checkbox("Use container width", value=False, key="use_container_width")
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
                                [verkeerde_ritten],
                              [lijn_onder_capaciteit],
                              [lijn_boven_capaciteit],
                              'in te vullen eis 5*******',
                              'in te vullen eis 6*******',
                                'in te vullen eis 7*******',
                                'in te vullen eis 8*******',
                                'in te vullen eis 9*******'],})
    
    
    
    
    # Pie chart Eisen met totaal aantal counters
    st.subheader('Pie chart Eisen')
    labels_eisen = 'Eis 1', 'Eis 2', 'Eis 3','Eis 4','Eis 5','Eis 6','Eis 7','Eis 8','Eis 9'
    sizes_eisen = [counter1, counter2, counter3, counter4, counter5, counter6, counter7, counter8, counter9]
    
    # fig1, ax1 = plt.subplots()
    # ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
    #     shadow=True, startangle=90)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    fig_eisen = px.pie(values=sizes_eisen, names = labels_eisen, title = 'Eisen')
    st.plotly_chart(fig_eisen)
    
    ############################# FICTIEVE WAARDE
    counter1w = 2
    counter2w = 3
    counter3w = 5
    #############################
    
    # Pie chart Wensen met totaal aantal counters
    st.subheader('Pie chart Wensen')
    labels_wensen = 'Wens 1', 'Wens 2', 'Wens 3'
    sizes_wensen = [counter1w, counter2w, counter3w]

    fig_wensen = px.pie(values=sizes_wensen, names = labels_wensen, title = 'Wensen')
    st.plotly_chart(fig_wensen)
    
    
    
    ################################################ ALS EEN WAARDEN GROTER IS DAN 1 --> UITLEG GEVEN
    #################################################################################################
    
    st.subheader('Beschrijving van de Eisen')
    
    if counter1 > 0:
        st.markdown('beschrijving Eis 1')
        st.text_area('Eis 1', '''Eis 1 was gemaakt om te checken of er inderdaad 
        een bus rijdt op de momenten die vastgelegd zijn in de 
        dienstregeling.
        De rede dat er niet aan Eis 1 wordt voldaan is omdat er ............''')
        
    if counter2 > 0:
        st.markdown('beschrijving Eis 2')
        st.text_area('Eis 2', '''.....................''')
        
        
    if counter3 > 0:
        st.markdown('beschrijving Eis 3')
        st.text_area('Eis 3', '''.....................''')
        
    if counter4 > 0:
        st.markdown('beschrijving Eis 4')
        st.text_area('Eis 4', '''.....................''')
        
    if counter5 > 0:
        st.markdown('beschrijving Eis 5')
        st.text_area('Eis 5', '''.....................''')
    
    if counter6 > 0:
        st.markdown('beschrijving Eis 6')
        st.text_area('Eis 6', '''.....................''')
        
    if counter7 > 0:
        st.markdown('beschrijving Eis 7')
        st.text_area('Eis 7', '''.....................''')
    
    if counter8 > 0:
        st.markdown('beschrijving Eis 8')
        st.text_area('Eis 8', '''.....................''')
    
    if counter9 > 0:
        st.markdown('beschrijving Eis 9')
        st.text_area('Eis 9', '''.....................''')
        
        
        
        
    ################################################################################################################################

