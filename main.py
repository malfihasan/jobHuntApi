'''
last update     : 2025-06-07
author          : Alfi Hasan
project name    : Job Search Tool
local env       : webSD
'''
## importing libraries
import streamlit as st
import streamlit_antd_components as sac
from src.settings import LOGO_PATH
from src.lib_common import load_image
from src.company_screen import company_screen, top_10_screen

## Page Configuration
st.set_page_config(
    page_title="Job Search Tool",
    page_icon=":briefcase:",
    layout="wide",
)

## Sidebar Configuration
st.markdown(f'''
    <style>
    .stApp .main .block-container{{
        padding:30px 50px
    }}
    .stApp [data-testid='stSidebar']>div:nth-child(1)>div:nth-child(2){{
        padding-top:50px
    }}
    iframe{{
        display:block;
    }}
    .stRadio div[role='radiogroup']>label{{
        margin-right:5px
    }}
    </style>
    ''', unsafe_allow_html=True)

## Sidebar Menu
with st.sidebar.container():
    st.image(load_image(LOGO_PATH), use_column_width=True)
    st.markdown("<h1 style='text-align: center;'>Job Search Tool</h1>", unsafe_allow_html=True)
    menu = sac.menu(
        items=[
            #sac.MenuItem('Potential Company List', icon='list-alt'),
            sac.MenuItem('Top 10 Companies', icon='money-fill')
        ],
        key='menu',
        open_all=False, indent=20,
        format_func='title',
    )

## Main Page Connector
with st.container():
    if menu == 'Potential Company List':
        company_screen()
    if menu == 'Top 10 Companies':
        top_10_screen()


 
