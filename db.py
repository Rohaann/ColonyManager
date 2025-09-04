import sqlite3

def init_db():
    conn = sqlite3.connect("colony_manager.db")
    c = conn.cursor()

    # Colonies
    c.execute("""
    CREATE TABLE IF NOT EXISTS colonies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT
    )
    """)

    # Plots
    c.execute("""
    CREATE TABLE IF NOT EXISTS plots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        colony_id INTEGER,
        plot_no TEXT,
        size INTEGER,
        price REAL,
        status TEXT DEFAULT 'Available',
        customer_id INTEGER,
        release_date TEXT,
        FOREIGN KEY(colony_id) REFERENCES colonies(id)
    )
    """)

    # Customers
    c.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        email TEXT
    )
    """)

    # Payments
    c.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        plot_id INTEGER,
        amount REAL,
        mode TEXT,
        date TEXT,
        notes TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(id),
        FOREIGN KEY(plot_id) REFERENCES plots(id)
    )
    """)

    conn.commit()
    conn.close()
