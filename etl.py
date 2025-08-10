
import sqlite3
import pandas as pd
from pathlib import Path

def load_csv_to_sqlite(csv_path, table_name, conn):
    df = pd.read_csv(csv_path, parse_dates=True)
    df.to_sql(table_name, conn, if_exists='replace', index=False)

def main(db_path='data/processed/crm.db'):
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create tables
    with open('sql/schema.sql','r') as f:
        cur.executescript(f.read())

    # Load CSVs
    load_csv_to_sqlite('data/raw/customers.csv','customers', conn)
    load_csv_to_sqlite('data/raw/orders.csv','orders', conn)
    load_csv_to_sqlite('data/raw/interactions.csv','interactions', conn)
    load_csv_to_sqlite('data/raw/support_tickets.csv','support_tickets', conn)
    load_csv_to_sqlite('data/raw/email_events.csv','email_events', conn)
    load_csv_to_sqlite('data/raw/subscriptions.csv','subscriptions', conn)

    conn.commit()
    conn.close()
    print('Loaded CSVs into SQLite at', db_path)

if __name__ == '__main__':
    main()
