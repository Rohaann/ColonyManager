import streamlit as st
import sqlite3
from db import init_db

init_db()

def get_connection():
    return sqlite3.connect("colony_manager.db")

st.set_page_config(page_title="Colony Manager", layout="wide")
st.title("🏡 Colony Manager")

menu = ["Dashboard", "Colonies", "Plots", "Customers", "Payments"]
choice = st.sidebar.radio("Go to", menu)

conn = get_connection()
c = conn.cursor()

# Dashboard
if choice == "Dashboard":
    st.subheader("📊 Dashboard")
    total_colonies = c.execute("SELECT COUNT(*) FROM colonies").fetchone()[0]
    total_plots = c.execute("SELECT COUNT(*) FROM plots").fetchone()[0]
    total_customers = c.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    total_payments = c.execute("SELECT SUM(amount) FROM payments").fetchone()[0] or 0

    st.metric("Total Colonies", total_colonies)
    st.metric("Total Plots", total_plots)
    st.metric("Customers", total_customers)
    st.metric("Payments Received", f"₹ {total_payments:,.2f}")

# Colonies
elif choice == "Colonies":
    st.subheader("🏘️ Colonies")
    with st.form("Add Colony"):
        name = st.text_input("Colony Name")
        location = st.text_input("Location")
        submit = st.form_submit_button("Add")
        if submit:
            c.execute("INSERT INTO colonies (name, location) VALUES (?, ?)", (name, location))
            conn.commit()
            st.success(f"Colony '{name}' added!")

    st.write("### Colony List")
    colonies = c.execute("SELECT * FROM colonies").fetchall()
    st.table(colonies)

# Plots
elif choice == "Plots":
    st.subheader("📐 Plots")
    colonies = c.execute("SELECT id, name FROM colonies").fetchall()
    colony_map = {str(cid): cname for cid, cname in colonies}

    with st.form("Add Plot"):
        colony_id = st.selectbox("Colony", list(colony_map.keys()), format_func=lambda x: colony_map[x])
        plot_no = st.text_input("Plot Number")
        size = st.number_input("Size (sqft)", min_value=0)
        price = st.number_input("Price", min_value=0.0)
        status = st.selectbox("Status", ["Available", "Booked", "Mortgage", "Released"])
        release_date = st.date_input("Release Date (if Mortgage)", value=None)
        submit = st.form_submit_button("Add Plot")
        if submit:
            c.execute("INSERT INTO plots (colony_id, plot_no, size, price, status, release_date) VALUES (?, ?, ?, ?, ?, ?)",
                      (colony_id, plot_no, size, price, status, str(release_date)))
            conn.commit()
            st.success(f"Plot {plot_no} added!")

    st.write("### Plots List")
    plots = c.execute("SELECT * FROM plots").fetchall()
    st.table(plots)

# Customers
elif choice == "Customers":
    st.subheader("👥 Customers")
    with st.form("Add Customer"):
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        submit = st.form_submit_button("Add Customer")
        if submit:
            c.execute("INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
            conn.commit()
            st.success(f"Customer '{name}' added!")

    st.write("### Customer List")
    customers = c.execute("SELECT * FROM customers").fetchall()
    st.table(customers)

# Payments
elif choice == "Payments":
    st.subheader("💰 Payments")
    customers = c.execute("SELECT id, name FROM customers").fetchall()
    plots = c.execute("SELECT id, plot_no FROM plots").fetchall()
    cust_map = {str(cid): cname for cid, cname in customers}
    plot_map = {str(pid): pno for pid, pno in plots}

    with st.form("Add Payment"):
        customer_id = st.selectbox("Customer", list(cust_map.keys()), format_func=lambda x: cust_map[x])
        plot_id = st.selectbox("Plot", list(plot_map.keys()), format_func=lambda x: plot_map[x])
        amount = st.number_input("Amount", min_value=0.0)
        mode = st.text_input("Payment Mode")
        date = st.date_input("Date")
        notes = st.text_area("Notes")
        submit = st.form_submit_button("Record Payment")
        if submit:
            c.execute("INSERT INTO payments (customer_id, plot_id, amount, mode, date, notes) VALUES (?, ?, ?, ?, ?, ?)",
                      (customer_id, plot_id, amount, mode, str(date), notes))
            conn.commit()
            st.success("Payment recorded!")

    st.write("### Payment History")
    payments = c.execute("SELECT * FROM payments").fetchall()
    st.table(payments)

conn.close()
