
import streamlit as st, json, os, uuid
from datetime import datetime

DB='items.json'

def load():
    if os.path.exists(DB):
        return json.load(open(DB))
    return []

def save(x):
    json.dump(x, open(DB,'w'), indent=2)

st.set_page_config(page_title='MU Lost & Found', layout='wide')

if 'logged_in' not in st.session_state:
    st.session_state.logged_in=False

if not st.session_state.logged_in:
    st.title('🎒 Mahindra University Lost & Found')
    roll=st.text_input('Roll Number')
    name=st.text_input('Name')
    if st.button('Login'):
        if roll.upper().startswith('SM'):
            st.session_state.logged_in=True
            st.session_state.roll=roll.upper()
            st.session_state.name=name
            st.rerun()
        else:
            st.error('Only SM roll numbers allowed')
    st.stop()

data=load()

page=st.sidebar.selectbox('Menu',['Browse Items','Post Item','My Posts'])

if page=='Browse Items':
    st.title('Browse Items')
    q=st.text_input('Search')
    cat=st.selectbox('Category',['All','Lost','Found'])
    items=data
    if cat!='All':
        items=[i for i in items if i['category']==cat]
    if q:
        items=[i for i in items if q.lower() in str(i).lower()]
    for i in reversed(items):
        with st.container(border=True):
            st.subheader(i['title'])
            st.write(i['description'])
            st.write('Location:', i['location'])
            st.write('Contact:', i['contact'])

elif page=='Post Item':
    st.title('Post Item')
    category=st.selectbox('Type',['Lost','Found'])
    title=st.text_input('Title')
    description=st.text_area('Description')
    location=st.text_input('Location')
    contact=st.text_input('Contact')
    if st.button('Submit'):
        data.append({
            'category':category,
            'title':title,
            'description':description,
            'location':location,
            'contact':contact,
            'roll':st.session_state.roll,
            'date':datetime.now().isoformat()
        })
        save(data)
        st.success('Posted')

else:
    st.title('My Posts')
    for i in data:
        if i['roll']==st.session_state.roll:
            st.write(i['title'])
