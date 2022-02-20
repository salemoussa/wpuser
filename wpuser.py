import requests
import json
import pandas as pd
import streamlit as st
from json.decoder import JSONDecodeError

st.title('Wordpress Usernames Finder')
st.write("Input full URL below to pull website's usernames")
with st.form("my_form"):
   source = st.text_input('https://example.com', value='' , max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False),
   submitted = st.form_submit_button(label='Lookup')
if submitted:
  try:
    convert = ''.join(source)
    stripped = convert.strip('('',)')
    url = "{}/wp-json/wp/v2/users/".format(stripped)
    r = requests.get(url)
    cont = r.json()
    df = pd.DataFrame(cont)
    df.drop(['_links', 'slug', 'url', 'link', 'meta', 'avatar_urls'], axis=1, inplace=True)
    df = df.rename(columns={'id': 'User_ID', 'name': 'WP_username', 'User_description': 'User_Description'})
    df.reset_index(drop=True, inplace=True)
    st.write('Total number of users: ', len(df))
    st.dataframe(df)
  except ValueError:
    st.warning('FAILED: website is not using wordpress or have extra security to hide usernames. Try another one')
