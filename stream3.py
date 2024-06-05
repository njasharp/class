import streamlit as st
import pandas as pd

st.set_page_config (layout="wide")

#header - header of the app 
st.header("Using streamlit input widgets ")


reg_form = st.form("user_registration_form")
first_name = reg_form.text_input('First Name: ', key='fname')
last_name = reg_form.text_input('Last Name: ', key='Lname')
password = reg_form.text_input('Password: ', type='password', key='password')
age = reg_form.slider("What is your current age?")
level = reg_form.radio("What is your membership level?", ['Silver', 'Gold', 'Platinum'])
status = reg_form.checkbox("Active Member?")
submit_button = reg_form.form_submit_button('Submit')

if submit_button:
    st.success('Welcome' + ' ' + first_name + " " + last_name + ". you are a  valued " + level + " member.")


df = pd.read_csv(r"data1.csv")
st.write(df)
dc = {"a" : 10, "b" : 20, "c" : 30}
st.write(dc)