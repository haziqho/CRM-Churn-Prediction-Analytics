
import sqlite3
import pandas as pd
from pathlib import Path

AS_OF = '2025-07-31'

def main(db_path='data/processed/crm.db', out_csv='data/processed/features.csv'):
    conn = sqlite3.connect(db_path)

    # RFM
    rfm = pd.read_sql_query(f"""
    WITH order_stats AS (
      SELECT o.customer_id,
             COUNT(*) AS order_count,
             SUM(o.amount) AS total_spend,
             MAX(o.order_date) AS last_order_date
      FROM orders o
      GROUP BY o.customer_id
    )
    SELECT c.customer_id,
           julianday('{AS_OF}') - julianday(last_order_date) AS recency_days,
           COALESCE(order_count,0) AS frequency,
           COALESCE(total_spend,0) AS monetary
    FROM customers c
    LEFT JOIN order_stats os ON c.customer_id=os.customer_id
    """, conn)

    # Support (90d)
    support = pd.read_sql_query(f"""
    SELECT c.customer_id,
           SUM(CASE WHEN DATE(opened_at) >= DATE('{AS_OF}', '-90 day') THEN 1 ELSE 0 END) AS tickets_90d
    FROM customers c LEFT JOIN support_tickets s ON c.customer_id=s.customer_id
    GROUP BY c.customer_id
    """, conn)

    # Email engagement
    email = pd.read_sql_query("""
    WITH email_counts AS (
      SELECT customer_id,
             SUM(CASE WHEN event_type='open' THEN 1 ELSE 0 END) AS opens,
             SUM(CASE WHEN event_type='click' THEN 1 ELSE 0 END) AS clicks,
             SUM(CASE WHEN event_type='sent' THEN 1 ELSE 0 END) AS sent
      FROM email_events GROUP BY customer_id
    )
    SELECT c.customer_id,
           CASE WHEN sent>0 THEN 1.0*opens/sent ELSE 0 END AS open_rate,
           CASE WHEN sent>0 THEN 1.0*clicks/sent ELSE 0 END AS click_rate
    FROM customers c LEFT JOIN email_counts e ON c.customer_id=e.customer_id
    """, conn)

    # Interactions (30d)
    inter = pd.read_sql_query(f"""
    SELECT c.customer_id,
           SUM(CASE WHEN DATE(i.date) >= DATE('{AS_OF}', '-30 day') THEN 1 ELSE 0 END) AS interactions_30d
    FROM customers c LEFT JOIN interactions i ON c.customer_id=i.customer_id
    GROUP BY c.customer_id
    """, conn)

    # Label
    label = pd.read_sql_query("SELECT customer_id, is_churned FROM subscriptions", conn)

    # Merge
    df = rfm.merge(support, on='customer_id', how='left')\
            .merge(email, on='customer_id', how='left')\
            .merge(inter, on='customer_id', how='left')\
            .merge(label, on='customer_id', how='left')

    df = df.fillna(0)
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    print('Wrote features to', out_csv)

if __name__ == '__main__':
    main()
