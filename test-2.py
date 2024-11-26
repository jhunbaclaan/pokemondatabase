import streamlit as st
import pypokedex as pokedex
import pandas as pd
import requests
import csv
import os
import matplotlib.pyplot as plt
from test import get_sets, get_box
from user import User

# Set page configuration to wide mode
st.set_page_config(layout='wide')

league_file = 'league.csv'
league_df = pd.DataFrame()
league_df = pd.read_csv(league_file)

set_file = 'set.csv'
set_df = pd.DataFrame()
set_df = pd.read_csv(set_file)

user_file = 'user.csv'
user_df = pd.DataFrame()
user_df = pd.read_csv(user_file)

pokemon_file = 'pokemon.csv'
pokemon_df = pd.DataFrame()
pokemon_df = pd.read_csv(pokemon_file)

pokemonbox_file = 'pokemonbox.csv'
pokemonbox_df = pd.DataFrame()
pokemonbox_df = pd.read_csv(pokemonbox_file)
pokemonbox_df = pokemonbox_df.drop(columns=['Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5'])

match_file = 'match.csv'
match_df = pd.DataFrame()
match_df = pd.read_csv(match_file)

#st.dataframe(league_df)

if 'user_portal' not in st.session_state:
    st.session_state['user_portal'] = True
if 'league_host_screen' not in st.session_state:
    st.session_state['league_host_screen'] = False
if 'league_user_screen' not in st.session_state:
    st.session_state['league_user_screen'] = False
if 'host_flag' not in st.session_state:
    st.session_state.host_flag = False
if 'league_id' not in st.session_state:
    st.session_state.league_id = ''
if 'user_id' not in st.session_state:
    st.session_state.user_id = ''
if 'user_df' not in st.session_state:
    st.session_state.user_df = pd.DataFrame()
if 'league_df' not in st.session_state:
    st.session_state.league_df = pd.DataFrame()

host_flag = st.session_state.host_flag
league_id = st.session_state.league_id

if not st.session_state.league_df.empty:
    league_df = st.session_state.league_df

# runs as first page
if st.session_state['user_portal']:

    # ui
    st.title('Pokemon Draft League Portal')

    # sets up column objects
    col1, col2 = st.columns([1, 0.5])

    # input ui
    with col2:  
        st.write('')
        host_flag = st.checkbox('Are you the host?', key='hf')
    with col1:
        league_id = st.text_input('Enter League ID you are searching for', key='lid_in')
    

    if league_id != '':

        # verifies input was an int
        try:
            league_id = int(league_id)
        except Exception as e:
            st.write('Error: Input a number')
            st.stop()

        # verifies league id exists
        if league_id not in league_df.League_ID.tolist():
            st.write('This League ID does not exist')
            st.stop()
        else:
            league_df = league_df[league_df['League_ID'] == league_id]
            user_df = user_df[user_df['League_ID'] == league_id]
            #st.dataframe(league_df)

        if host_flag:

            host_id = st.text_input('Enter your host passkey (User ID)')

            # stop run until host_id is inputted
            if host_id != '':

                try:
                    host_id = int(host_id)
                except Exception as e:
                    st.write('Error: Input a number')
                    st.stop()
    
                if host_id not in league_df.Host_ID.tolist():
                    st.write('This User ID is not host of this league')
                    st.write('If you are not the user unselect the Host checkbox')
                    st.stop()

                else:
                    st.write('Click to view your League')
                    st.button('Continue')
                    st.session_state.league_df = league_df
                    st.session_state['league_host_screen'] = True
                    st.session_state['user_portal'] = False
                    st.rerun()
        else:

            user_id = st.text_input('Enter your User ID')

            # stop run until host_id is inputted
            if user_id != '':

                try:
                    user_id = int(user_id)
                except Exception as e:
                    st.write('Error: Input a number')
                    st.stop()
    
                if user_id not in user_df.User_ID.tolist():
                    st.write('This User ID is not in this league')
                    st.write('Only user in this league can view the league info')
                    st.stop()

                else:
                    st.write('Click to view your League')
                    st.button('Continue')
                    st.session_state.user_id = user_id
                    st.session_state.league_df = league_df
                    st.session_state['league_user_screen'] = True
                    st.session_state['user_portal'] = False
                    st.rerun()

elif st.session_state['league_host_screen']:
    st.title(league_df.League_Name.tolist()[0])

elif st.session_state['league_user_screen']:
    
    user_df_queried = user_df[user_df['User_ID'] == st.session_state.user_id].reset_index()
    user = user_df_queried['User_FirstName'].tolist()[0]
    other_user = None
    
    st.title(f'Hi {user}, here is your {league_df.League_Name.tolist()[0]} league')

    st.header('Your Profile:')
    
    with st.expander('View your match history'):

        your_set = get_sets(user, set_df, match_df, user_df)
        
        wins = len([ res for res in your_set.Match_Result.tolist() if res == 'W'])
        losses = len([ res for res in your_set.Match_Result.tolist() if res == 'L'])
        record = f'{wins}-{losses}'
        
        st.header(f"Your match history")
        st.subheader(f'Overall Record: {record}')

        st.dataframe(your_set)
        
    with st.expander('View your Pokemon'):
        st.header(f"Your Pokemon:")
        st.write('___________________________________________________________________________________')
        get_box(user, user_df, pokemon_df, pokemonbox_df)

    st.header('View other user profiles:')

    with st.expander("View other user's match histories"):

        other_user_m = st.selectbox('Select a user', user_df.User_FirstName.tolist(), index=None, key='othuserm')

        if other_user_m is not None:
            
            their_set = get_sets(other_user_m, set_df, match_df, user_df)
            
            wins = len([ res for res in their_set.Match_Result.tolist() if res == 'W'])
            losses = len([ res for res in their_set.Match_Result.tolist() if res == 'L'])
            record = f'{wins}-{losses}'
            
            st.header(f"{other_user_m}'s match history")
            st.subheader(f'Overall Record: {record}')
    
            st.dataframe(your_set)
        
    with st.expander("View other user's pokemon"):

        other_user = st.selectbox('Select a user', user_df.User_FirstName.tolist(), index=None, key='othuserp')

        if other_user is None:
            st.stop()
        
        st.header(f"{other_user}'s Pokemon:")
        st.write('___________________________________________________________________________________')
        get_box(other_user, user_df, pokemon_df, pokemonbox_df)
    
    st.stop()
    st.title(f"{other_user}'s Pokemon:")
    st.write('___________________________________________________________________________________')

