from dotenv import load_dotenv
#load_dotenv() ## Load all the environment variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai
## Configure GenAI Key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load google_gemini model and provide queries as response

def get_gemini_response(question,prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0],question])
    
    return response.text

## Function to retrieve query from the database

def read_sql_query(sql,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    print('now executing:')
    for row in rows:
        print(row)
    conn.close()
    return rows

## Define prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query! 
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION \n\n
    For example,\n
    Example 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ; \n
    Example 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT where CLASS="Data Science"; \n
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]


## Streamlit App

st.set_page_config(page_title="I can retrieve any SQL query")
st.header("Gemini App to Retrieve SQL Data")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_gemini_response(question,prompt)
    print(response)
    st.write('The SQL command applied:')
    st.write(response)
    result = read_sql_query(response,'student.db')
    st.subheader("The response is: ")
    for row in result:
        #print(row)
        st.header(row)
                                      