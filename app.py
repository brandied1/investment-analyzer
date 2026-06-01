import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Investment Analyzer",
    layout="wide"
)

st.title("Investment Analyzer")

df = pd.read_csv("rankings.csv")

st.subheader("S&P 500 Rankings")

search = st.text_input(
    "Search Company or Ticker"
)

if search:

    df = df[
        df["Ticker"].str.contains(
            search,
            case=False,
            na=False
        )
        |
        df["Company"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

st.dataframe(
    df,
    use_container_width=True
)