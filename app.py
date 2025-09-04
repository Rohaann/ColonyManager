import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# ---------------- Google Sheets Setup ----------------
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open("ColonyManagerDB")

colonies_ws = sheet.worksheet("Colonies")
plots_ws = sheet.worksheet("Plots")
customers_ws = sheet.worksheet("Customers")
payments_ws = sheet.worksheet("Payments")
mortgages_ws = sheet.worksheet("Mortgages")

# ---------------- Sidebar Menu ----------------
menu = st.sidebar.radio("📌 Navigation",
    ["Dashboard", "Colonies", "Plots", "Customers", "Payments", "Mortgages"])

# ---------------- Dashboard ----------------
if menu == "Dashboard":
    st.title("📊 Colony Manager Dashboard")

    # Load data
    plots = pd.DataFrame(plots_ws.get_all_records())
    mortgages = pd.DataFrame(mortgages_ws.get_all_records())

    if not plots.empty:
        total_plots = len(plots)
        available = len(plots[plots["Status"] == "Available"])
        sold = len(plots[plots["Status"] == "Sold"])

        # Mortgages count
        mortgaged = 0
        if not mortgages.empty:
            mortgaged = len(mortgages[mortgages["Status"] == "Mortgaged"])

        st.subheader("Overall Stats")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Plots", total_plots)
        col2.metric("Available", available)
        col3.metric("Sold", sold)
        col4.metric("Mortgaged", mortgaged)

        # Owner-wise
        st.subheader("Owner Breakdown")
        owners = plots.groupby("Owner")["Number"].count().reset_index()
        st.dataframe(owners)

    else:
        st.warning("No plots found. Please run setup first.")

# ---------------- Rest of your code (Colonies, Plots, Customers, Payments, Mortgages) ----------------
# Keep your existing forms and display logic for these sections
