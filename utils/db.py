import sqlite3

DB_NAME = "disasterguard.db"

# ---------------- CONNECT ----------------
def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# ---------------- INIT DB ----------------
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tracking_id TEXT,
        name TEXT,
        location TEXT,
        disaster_type TEXT,
        severity TEXT,
        description TEXT,
        image_path TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    conn.commit()
    conn.close()

# ---------------- ADD REPORT (REQUIRED BY YOUR PAGE) ----------------
def add_report(tracking_id, name, location, disaster_type, severity, description, image_path):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reports (
            tracking_id,
            name,
            location,
            disaster_type,
            severity,
            description,
            image_path,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending')
    """, (
        tracking_id,
        name,
        location,
        disaster_type,
        severity,
        description,
        image_path
    ))

    conn.commit()
    conn.close()

# ---------------- FETCH REPORTS ----------------
def fetch_reports():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM reports ORDER BY id DESC")
    rows = cur.fetchall()

    conn.close()
    return rows

# ---------------- GET REPORT ----------------
def get_report(tracking_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM reports WHERE tracking_id=?", (tracking_id,))
    row = cur.fetchone()

    conn.close()
    return row

# ---------------- UPDATE STATUS ----------------
def update_status(report_id, status):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE reports
        SET status=?
        WHERE id=?
    """, (status, report_id))

    conn.commit()
    conn.close()