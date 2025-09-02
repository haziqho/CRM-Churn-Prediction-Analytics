USE `CRM Churn`;   -- change if your schema is named differently

-- Drop the old view/table if it exists
DROP VIEW IF EXISTS churn_features_final;
DROP TABLE IF EXISTS churn_features_final;

-- Recreate the view cleanly (no header rows!)
CREATE OR REPLACE VIEW churn_features_final AS
SELECT
    c.customer_id,

    -- Orders (RFM features)
    IFNULL(r.order_count, 0) AS order_count,
    IFNULL(r.total_spend, 0) AS total_spend,
    DATEDIFF(CURDATE(), r.last_order_date) AS recency_days,

    -- Support tickets (last 90 days)
    IFNULL(s.tickets_last_90d, 0) AS tickets_last_90d,

    -- Email engagement
    IFNULL(e.open_rate, 0)  AS open_rate,
    IFNULL(e.click_rate, 0) AS click_rate,

    -- Interactions (last 30 days)
    IFNULL(i.interactions_30d, 0) AS interactions_30d,

    -- Churn label: 1 if no order in last 120 days
    CASE 
        WHEN DATEDIFF(CURDATE(), r.last_order_date) > 120 THEN 1
        ELSE 0
    END AS is_churned

FROM customers c

-- Orders (Recency, Frequency, Monetary)
LEFT JOIN (
    SELECT 
        customer_id,
        COUNT(*) AS order_count,
        SUM(amount) AS total_spend,
        MAX(order_date) AS last_order_date
    FROM orders
    GROUP BY customer_id
) r ON c.customer_id = r.customer_id

-- Support tickets (last 90 days)
LEFT JOIN (
    SELECT 
        customer_id,
        COUNT(*) AS tickets_last_90d
    FROM support_tickets
    WHERE opened_at >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
    GROUP BY customer_id
) s ON c.customer_id = s.customer_id

-- Email engagement
LEFT JOIN (
    SELECT
        customer_id,
        SUM(event_type='open')  / NULLIF(SUM(event_type='sent'),0) AS open_rate,
        SUM(event_type='click') / NULLIF(SUM(event_type='sent'),0) AS click_rate
    FROM email_events
    GROUP BY customer_id
) e ON c.customer_id = e.customer_id

-- Interactions (last 30 days)
LEFT JOIN (
    SELECT 
        customer_id,
        COUNT(*) AS interactions_30d
    FROM interactions
    WHERE date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    GROUP BY customer_id
) i ON c.customer_id = i.customer_id;
