import sqlite3


def create_connection():
    return sqlite3.connect("disasterguard.db")


def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        disaster_type TEXT,
        description TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS volunteers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        skill TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_report(name, phone, disaster_type, description):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reports
        (name, phone, disaster_type, description)
        VALUES (?, ?, ?, ?)
        """,
        (name, phone, disaster_type, description)
    )

    conn.commit()
    conn.close()


def save_volunteer(name, phone, skill):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO volunteers
        (name, phone, skill)
        VALUES (?, ?, ?)
        """,
        (name, phone, skill)
    )

    conn.commit()
    conn.close()