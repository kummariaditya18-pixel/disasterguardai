import pandas as pd
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(PROJECT_ROOT, "../data/reports.csv")


def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame()


def save_data(new_row: dict):
    df = load_data()

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
    df.to_csv(CSV_FILE, index=False)