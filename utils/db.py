import sqlite3

DB_NAME = "disasterguard.db"


# ---------------- CONNECTION ----------------
def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# ---------------- INIT DB ----------------
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
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
    """
    )

    conn.commit()
    conn.close()


# ---------------- ADD REPORT ----------------
def add_report(tracking_id, name, location, disaster_type, severity, description, image_path):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO reports (
            tracking_id, name, location,
            disaster_type, severity, description,
            image_path, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending')
    """,
        (tracking_id, name, location, disaster_type, severity, description, image_path),
    )

    conn.commit()
    conn.close()


# ---------------- FETCH ALL REPORTS ----------------
def fetch_reports():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM reports ORDER BY id DESC")
    rows = cur.fetchall()

    conn.close()
    return rows


# ---------------- GET SINGLE REPORT ----------------
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

    cur.execute("UPDATE reports SET status=? WHERE id=?", (status, report_id))

    conn.commit()
    conn.close()


# ---------------- COUNT REPORTS (FIXED ERROR) ----------------
def count_reports():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM reports")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM reports WHERE status='Pending'")
    pending = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM reports WHERE status='Rescued'")
    rescued = cur.fetchone()[0]

    conn.close()

    return total, pending, rescued
