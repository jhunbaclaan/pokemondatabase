# code for making your user:
import streamlit as st
import pymysql
import pandas as pd

# method to input new users
def insertUser(first_name, last_name, email):
    
    user_id = getUserID()
    
    query = f"""INSERT INTO Users (UserID, LeagueID, HostFlag, UserFirstName, UserLastName, UserEmail) VALUES({user_id}, {158}, {False}, "{first_name}", "{last_name}", "{email}");"""
    return query

# iterates through users to get new id
def getUserID():
    
    cursor.execute("""SELECT UserID FROM Users ORDER BY UserID DESC LIMIT 1;""")
    user_id = cursor.fetchall()[0][0] + 1

    return user_id 

# Replace these values with your actual connection details
host = '199.1.1.1'  # Public IP of your Google Cloud SQL MySQL instance
user = 'mkholck' # MySQL username (e.g., root)
password = '3G{6~A`TUO|xL\HT' # Leave this empty if there's no password
database = 'pokemon-draft-league' # The name of your database

# Establish the connection to Google Cloud SQL
db = pymysql.connect(
    host=host,
    user=user,
    password=password,  # Leave as an empty string if there's no password
    database=database,
    connect_timeout=60  # Increase the timeout to 30 seconds
)
cursor = db.cursor()
user_df = pd.DataFrame(columns=['First_Name', 'Last_Name', 'Email'])
st.title('Create User Profile')
first_name = st.text_input('Input your first name', key='fn')
last_name = st.text_input('Input your last name', key='ln')
email = st.text_input('Input your email', key='email')
# stops the query if values have not been inputted
if first_name is None or last_name is None or email is None:
    st.stop()
else:
    try:
        cursor.execute(insertUser(first_name, last_name, email))
        st.write('Your user profile has been created!')
	  
    except Exception as e:
        st.write(insertUser(first_name, last_name, email))
        st.write(f'An error occurred: {e}')
db.close()
