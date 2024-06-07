import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
from src.settings import *
from src.lib_common import load_css, get_csv, csv_save, process_df

def company_screen():
    load_css()

    ## Header
    with st.container():
        st.title("📊 Company Screener")
        st.write("---")

    targetDf = process_df()
    
    ## All Companies Data Table
    with st.container():
        st.header("🗃️ All Companies Data [Detail Tables]")
        AgGrid(targetDf, height=500, width='100%', fit_columns_on_grid_load=False)
    
    ## Company Selection Criteria
    with st.container():
        st.write("-------")
        st.header("📋 Company Selection Criteria")
        st.write("""
            - Revenue exceeding 1000 units
            - Profits greater than 100 units
            - Market Capitalization above 1000 units
            - Compliance with 'Halal' status
        """)
        st.write("-------")

        ## Filtered Companies
        selectedDf = targetDf[
            (targetDf['Revenue (in millions, USD)'] > 1000) &
            (targetDf['Profits (in millions, USD)'] > 100) &
            (targetDf['Valuation (in millions, USD)'] > 1000) &
            (targetDf['Status'] != 'NON-COMPLIANT')
        ]
        
        AgGrid(selectedDf, height=500, width='100%', fit_columns_on_grid_load=False)
        csv_save(selectedDf, "data/selected_companies.csv")

        ## Filtered Tech Companies
        st.write("-------")
        st.header("💻 Filtered Tech Companies")
        st.write("-------")

        selectedTechDf = selectedDf[selectedDf['Industry'].isin(['Technology', "Computers, Office Equipment", "Internet Services and Retailing", "Semiconductors and Other Electronic Components"])]
        AgGrid(selectedTechDf, height=500, width='100%', fit_columns_on_grid_load=False)
        csv_save(selectedTechDf, "data/selected_tech_companies.csv")

def top_10_screen():
    load_css()
    targetDf = process_df()

    ## Header
    with st.container():
        st.title("🏆 Top 10 Companies")
        st.write("---")

    ## Display Top 10 Companies in Two Columns
    col1, col2 = st.columns(2)

    with col1:
        display_top_companies(targetDf, "Revenue (in millions, USD)", "Top 10 Stable Companies", "Revenue")
        ## Display Top 10 Tech Companies
        with st.container():
            topTechDf = targetDf[targetDf['Industry'].isin(['Technology', "Computers, Office Equipment", "Internet Services and Retailing", "Semiconductors and Other Electronic Components"])]
            topTechDf = topTechDf.sort_values(by='Revenue (in millions, USD)', ascending=False).head(10)
            topTechDf = topTechDf[['Company', 'Industry', 'City', 'Revenue (in millions, USD)']]
            st.header("💻 Top 10 Tech Companies")
            AgGrid(topTechDf, width='100%', fit_columns_on_grid_load=False)
        
    with col2:
        display_top_companies(targetDf, "Valuation (in millions, USD)", "Top 10 Valued Companies", "Valuation")
        display_top_companies(targetDf, "Profits (in millions, USD)", "Top 10 Profiting Companies", "Profits")
        

        
def display_top_companies(dataframe, sortByColumn, header, columnDisplayName):
    selectedDf = dataframe.sort_values(by=sortByColumn, ascending=False).head(10)
    selectedDf = selectedDf[['Company', 'Industry', 'City', 'State', f'{columnDisplayName} (in millions, USD)']]
    with st.container():
        st.header(f"🏅 {header}")
        st.write("-------")
        AgGrid(selectedDf, width='100%', fit_columns_on_grid_load=False)

