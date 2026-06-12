import sqlite3

DB_NAME = "disasterguard.db"

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# ---------------- SAFE INIT (AUTO FIX OLD DB) ----------------
def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    # Create base table if not exists
    cursor.execute("""
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

    # 🔥 FIX: If old table exists without id, rebuild safely
    cursor.execute("PRAGMA table_info(reports)")
    columns = [col[1] for col in cursor.fetchall()]

    if "id" not in columns:
        cursor.execute("DROP TABLE reports")

        cursor.execute("""
        CREATE TABLE reports (
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

# ---------------- FETCH SAFE ----------------
def fetch_reports():
    conn = get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM reports ORDER BY id DESC")
        rows = cursor.fetchall()
    except Exception:
        # 🔥 fallback auto-repair
        init_db()
        cursor.execute("SELECT * FROM reports ORDER BY id DESC")
        rows = cursor.fetchall()

    conn.close()
    return rows

# ---------------- COUNTS ----------------
def count_reports():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reports")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE status='Pending'")
    pending = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE status='Rescued'")
    rescued = cursor.fetchone()[0]

    conn.close()
    return total, pending, rescued