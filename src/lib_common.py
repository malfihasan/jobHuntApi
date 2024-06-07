import json
import streamlit as st
import json
from PIL import Image
import pandas as pd

from src.settings import *

def load_css(file_name:str = "style/style.css"):
    ## load csss ##
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def load_image(image_name: str) -> Image:
    """Displays an image.

    Parameters
    ----------
    image_name : str
        Local path of the image.

    Returns
    -------
    Image
        Image to be displayed.
    """
    return Image.open(f"{image_name}")

def get_csv(file_name: str) -> pd.DataFrame:
    """Reads a CSV file.

    Parameters
    ----------
    file_name : str
        Local path of the CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the data from the CSV file.
    """
    return pd.read_csv(file_name)


## importing lotties gif  https://lottiefiles.com/animation/gif
def open_lottie(lotties_json = "data/sample_01.json"):
    with open(lotties_json, "r") as f:
        animation = json.load(f)
    return animation

def process_df()-> pd.DataFrame:
    ## Load SNP500 Data 
    fortDf = get_csv(FORT500_CSV_PATH )
    """
    print(fortDf.columns) 
    --->
    ['Rank', 'Company', 'Industry', 'City', 'State', 'Zip', 'Website',
    'Employees', 'Revenue (in millions, USD)',
    'Valuation (in millions, USD)', 'Profits (in millions, USD)',
    'Profits (% of Sales)', 'Ticker', 'CEO']
    """

    fortDf['Revenue (in millions, USD)'] = fortDf['Revenue (in millions, USD)'].str.replace(',', '').replace("$", "").astype(float)
    fortDf['Valuation (in millions, USD)'] = fortDf['Valuation (in millions, USD)'].str.replace(',', '').replace("$", "").astype(float)
    fortDf['Profits (in millions, USD)'] = fortDf['Profits (in millions, USD)'].str.replace(',', '').replace("$", "").astype(float)

    ## Load SNP500 Data
    snpDf = get_csv(SNP500_CSV_PATH)
    """
    print(snpDf.columns) 
    --->
    ['Rank', 'Ticker', 'Company', 'Market_Cap', 'Value', 'Change',
    'Revenues ']
    """
    snpDf['SNP500'] = True
    snpDf = snpDf[['Ticker', 'SNP500']]

    ## Merge 2 dataframes
    mergedDf = fortDf.merge(snpDf, left_on="Ticker", right_on="Ticker", how="left")

    ## Load filter data
    filterDf = get_csv(Filter_CSV_PATH)
    filterDf = filterDf[[ 'Symbol', 'Status']]
    """
    print(filterDf.columns)
    ['Rank', 'Symbol', 'Status', 'Price', 'MC']
    """

    ## Merge 2 dataframes
    mergedDf = mergedDf.merge(filterDf, left_on="Ticker", right_on="Symbol", how="left")

    ## drop duplicate rows
    mergedDf.drop_duplicates(subset=["Ticker"], inplace=True)

    return mergedDf

def csv_save(df: pd.DataFrame, file_name: str):
    df.to_csv(file_name, index=False)