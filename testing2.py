import streamlit as st
import pymysql
import pypokedex as pokedex
import pandas as pd
import requests
if 'draft_picks' not in st.session_state:
    st.session_state.draft_picks = []
if 'draft_pick_table' not in st.session_state:
    st.session_state.draft_pick_table = []
if 'picks_left' not in st.session_state:
    st.session_state.picks_left = 10
    
def get_rows_and_cols(picks):
    pick_table = []
    for row in range(0, len(picks), 6):
        pick_table.append(picks[row:row+6])
    return pick_table

def get_pokemon_num(pokemon):
    
    pmon = pokedex.get(name=pokemon)
    num = pmon.dex
    return num

def display_team(pick_table, image_gen):
    # get the columns in the array
    num_columns = len(pick_table[0])
    # iterate through the array:
    st.subheader('Your picks:')
    for row in pick_table:
        cols = st.columns(num_columns)
        for i, col in enumerate(cols):
            with col:
                if i >= len(row):
                    return
                poke_num = get_pokemon_num(row[i])
                st.image(f'{image_gen}{poke_num}.png', caption=row[i])
                      
db = pymysql.connect(
    # instantiate the database 
    host = "127.0.0.1",
    user = "root",
    password = "junesworld",
    database = "schema1"
    )
cursor = db.cursor()
                                
picks = st.session_state.draft_picks
image_gen = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"
st.title('Draft')
st.caption(f'You have {st.session_state.picks_left} picks left!')

pokemon_name = st.text_input('Insert the name of the pokemon you want to draft', key=f'name')

if st.session_state.picks_left <= 0:
    pick_table = get_rows_and_cols(picks)
    display_team(pick_table, image_gen)
    st.stop()

draft_confirm = st.button("Enter", key=f'draftbutton') # confirms all data in the form is stored

if draft_confirm and pokemon_name:
    
    if pokemon_name in picks:
        st.warning('This pokemon was selected already')
        pick_table = get_rows_and_cols(picks)
        display_team(pick_table, image_gen)
        st.stop()
    
    picks.append(pokemon_name.title())
    pick_table = get_rows_and_cols(picks)
    display_team(pick_table, image_gen)
    st.session_state.picks_left -= 1
    

