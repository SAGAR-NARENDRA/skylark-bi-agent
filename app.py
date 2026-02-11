
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Skylark BI Agent", layout="wide")

MONDAY_API_TOKEN = st.secrets.get("MONDAY_API_TOKEN", os.getenv("MONDAY_API_TOKEN"))
WORK_BOARD_ID = st.secrets.get("WORK_BOARD_ID", os.getenv("WORK_BOARD_ID"))
DEALS_BOARD_ID = st.secrets.get("DEALS_BOARD_ID", os.getenv("DEALS_BOARD_ID"))

def fetch_board(board_id):
    query = f'''
    query {{
      boards(ids: {board_id}) {{
        items_page(limit: 500) {{
          items {{
            id
            name
            column_values {{
              id
              text
              value
            }}
          }}
        }}
      }}
    }}
    '''
    headers = {
        "Authorization": MONDAY_API_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.post(
        "https://api.monday.com/v2",
        json={"query": query},
        headers=headers
    )
    data = response.json()
    items = data["data"]["boards"][0]["items_page"]["items"]
    records = []
    for item in items:
        record = {"name": item["name"]}
        for col in item["column_values"]:
            record[col["id"]] = col["text"]
        records.append(record)
    return pd.DataFrame(records)

def clean_dates(df):
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

def revenue_summary(deals_df):
    numeric_cols = deals_df.select_dtypes(include="object").columns
    for col in numeric_cols:
        try:
            deals_df[col] = deals_df[col].str.replace(",", "").str.replace("$", "")
            deals_df[col] = pd.to_numeric(deals_df[col])
        except:
            pass
    numeric_df = deals_df.select_dtypes(include="number")
    total_revenue = numeric_df.sum().sum()
    return total_revenue

st.title("🚀 Skylark Monday.com BI Agent")

if not MONDAY_API_TOKEN or not WORK_BOARD_ID or not DEALS_BOARD_ID:
    st.warning("Please configure MONDAY_API_TOKEN, WORK_BOARD_ID, and DEALS_BOARD_ID in Streamlit secrets.")
    st.stop()

with st.spinner("Fetching live data from Monday.com..."):
    work_df = fetch_board(WORK_BOARD_ID)
    deals_df = fetch_board(DEALS_BOARD_ID)

work_df = clean_dates(work_df)
deals_df = clean_dates(deals_df)

st.subheader("Ask a Business Question")
query = st.text_input("Example: How is our revenue looking?")

if query:
    if "revenue" in query.lower():
        total = revenue_summary(deals_df)
        st.success(f"Total Pipeline Revenue (All Numeric Fields Summed): ${total:,.2f}")
        st.info("Note: Revenue calculated from numeric columns in Deals board.")
    elif "work" in query.lower() or "execution" in query.lower():
        st.success(f"Total Work Orders: {len(work_df)}")
    else:
        st.info("Basic demo agent. Try asking about revenue or work orders.")

st.divider()
st.subheader("Data Preview")
st.write("Work Orders Board")
st.dataframe(work_df.head())
st.write("Deals Board")
st.dataframe(deals_df.head())
