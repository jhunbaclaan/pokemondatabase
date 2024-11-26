import streamlit as st
import pypokedex as pokedex
import pandas as pd
import requests
import csv
import os
import matplotlib.pyplot as plt

def get_sets(user, set_df, match_df, user_df):
    
    temp_set_df = pd.merge(set_df, match_df, on='Match_ID', how='inner')
    #st.dataframe(temp_set_df)
    
    temp_set_df1 = temp_set_df.drop(columns=['Player2_ID'])
    temp_set_df1 = temp_set_df1.rename(columns={'Player1_ID' : 'User_ID'})
    #st.dataframe(temp_set_df1)
    
    temp_set_df2 = temp_set_df.drop(columns=['Player1_ID'])
    temp_set_df2 = temp_set_df2.rename(columns={'Player2_ID' : 'User_ID'})
    temp_set_df2['Match_Result'] = temp_set_df1['Match_Result'].apply(lambda res: 'W' if res == 'L' else 'L')
    
    #st.dataframe(temp_set_df2)
    
    new_set_df1 = pd.merge(temp_set_df1, user_df, on='User_ID', how='inner')
    new_set_df2 = pd.merge(temp_set_df2, user_df, on='User_ID', how='inner')
    
    vs_user = new_set_df2[['Set_ID', 'User_FirstName']]
    
    new_set_df1 = new_set_df1[['Set_ID', 'Match_number', 'Match_Result', 'Match_Date', 'User_FirstName']]
    user_set= new_set_df1.query(f'User_FirstName == "{user}"')
    user_set = pd.merge(user_set, vs_user, on='Set_ID', how='inner')
    
    user_set = user_set.query(f'User_FirstName_y != "{user}"')
    user_set = (user_set.drop_duplicates(subset=['Match_number'], keep='first')).reset_index(drop=True)
    user_set = user_set.drop(columns=['User_FirstName_x'])
    user_set = user_set.rename(columns={'User_FirstName_y' : 'Opponent'})
    
    return user_set

#st.dataframe(new_set_df1)
#st.dataframe(new_set_df2)

def get_box(user, user_df, pokemon_df, pokemonbox_df):

    user_df_to_join = user_df[['User_ID', 'User_FirstName']]
    pokemon_df_to_join = pokemon_df[['Pokemon_ID', 'Pokemon_Name']]
    temp_pokemonbox_df = pd.merge(pokemonbox_df, user_df_to_join, on='User_ID', how='inner')
    new_pokemonbox_df = pd.merge(temp_pokemonbox_df, pokemon_df_to_join, on='Pokemon_ID', how='inner')
    
    
    logan_pokemonbox = new_pokemonbox_df.query(f'User_FirstName == "{user}"').reset_index()
    logan_pokemonbox = logan_pokemonbox[['Pokemon_Name']]

    if user == 'Logan':
        logan_pokemonbox['Pokemon_Name'] = [ name.replace('Victreebell', 'Victreebel')for name in logan_pokemonbox['Pokemon_Name'] ]
    if user == 'Matt':
         logan_pokemonbox['Pokemon_Name'] = [ name.replace('Toxtricity', 'Toxtricity-Low-Key')for name in logan_pokemonbox['Pokemon_Name'] ]
    if user == 'Colin':
         logan_pokemonbox['Pokemon_Name'] = [ name.replace('Morpeko', 'Morpeko-full-belly')for name in logan_pokemonbox['Pokemon_Name'] ]
         logan_pokemonbox['Pokemon_Name'] = [ name.replace('Enamorus', 'Enamorus-Therian')for name in logan_pokemonbox['Pokemon_Name'] ]

    image_gen = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"
    num_columns = len(logan_pokemonbox['Pokemon_Name'])
    cols = st.columns(num_columns)
    
    
    for i, col in enumerate(cols):
        with col:
            st.image(f'{image_gen}{pokedex.get(name=logan_pokemonbox["Pokemon_Name"].loc[i]).dex}.png',
                     caption=logan_pokemonbox["Pokemon_Name"].loc[i])
    for pokemon in logan_pokemonbox['Pokemon_Name']:
        st.write('___________________________________________________________________________________')
        st.subheader(pokemon)
        col1, col2 = st.columns([0.5, 1])
        with col1:
            st.image(f'{image_gen}{pokedex.get(name=pokemon).dex}.png', caption=pokemon, width=400)
        with col2:
            st.subheader('')
            stat_dict = pokedex.get(name=pokemon).base_stats
    
            stats_cols = ['HP', 'Attack', 'Defense', 'Special Attack', 'Special Defense', 'Speed']
            stat_df = pd.DataFrame(columns=['Stats'], data=pokedex.get(name=pokemon).base_stats, index=stats_cols)
    
            st.dataframe(stat_df)
