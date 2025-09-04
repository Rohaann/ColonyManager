import gspread
from google.oauth2.service_account import Credentials

# Define Google API scopes
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Authenticate with service account
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Open your Google Sheet
sheet = client.open("ColonyManagerDB")

# ---------------- Colonies ----------------
try:
    colonies_ws = sheet.worksheet("Colonies")
except:
    colonies_ws = sheet.add_worksheet(title="Colonies", rows="100", cols="10")

colonies_ws.update("A1:B1", [["Name", "Location"]])
colonies_ws.update("A2:B2", [["Kathaphod", "Devas"]])

# ---------------- Plots ----------------
# ---------------- Plots ----------------
try:
    plots_ws = sheet.worksheet("Plots")
except:
    plots_ws = sheet.add_worksheet(title="Plots", rows="500", cols="10")

# Clear old data first
plots_ws.clear()

# Add headers
plots_ws.update("A1:D1", [["Colony", "Number", "Status", "Owner"]])

# Add 180 plots
rows = [["Kathaphod", i, "Available", "Me"] for i in range(1, 181)]
plots_ws.append_rows(rows)

# ---------------- Customers ----------------
try:
    customers_ws = sheet.worksheet("Customers")
except:
    customers_ws = sheet.add_worksheet(title="Customers", rows="100", cols="10")

customers_ws.update("A1:B1", [["Name", "Contact"]])

# ---------------- Payments ----------------
try:
    payments_ws = sheet.worksheet("Payments")
except:
    payments_ws = sheet.add_worksheet(title="Payments", rows="200", cols="10")

payments_ws.update("A1:C1", [["Customer", "Plot", "Amount"]])

# ---------------- Mortgages ----------------
try:
    mortgages_ws = sheet.worksheet("Mortgages")
except:
    mortgages_ws = sheet.add_worksheet(title="Mortgages", rows="200", cols="10")

mortgages_ws.update("A1:E1", [["Colony", "Plot", "Owner", "Status", "Release Date"]])

print("✅ Setup complete! All 5 sheets created and initialized.")
