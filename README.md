
# CRM Churn Analytics with SQL + Python

Beginner-friendly end-to-end project that uses **SQL** and **Python** to:
- Load CRM-style data (orders, interactions, support tickets, email events)
- Build features with SQL (RFM, engagement, support burden)
- Train a **churn prediction** model (logistic regression / random forest)
- Automate the pipeline end-to-end

## Repository Structure
```
crm_sql_python_project/
├─ data/
│  ├─ raw/                # synthetic CSVs you can replace with real CRM exports
│  └─ processed/          # SQLite db, features & predictions
├─ sql/
│  ├─ schema.sql          # Tables
│  └─ queries.sql         # Example analytical queries
├─ src/
│  ├─ etl.py              # Load CSVs -> SQLite
│  ├─ build_features.py   # SQL feature engineering -> features.csv
│  ├─ train_model.py      # Train models + save predictions
│  └─ automate.py         # Orchestrate the whole pipeline
├─ models/                # saved model(s)
└─ README.md
```

## Quickstart
1. **Create & activate a virtual env (optional)**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

2. **Install packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the full pipeline**
   ```bash
   python src/automate.py
   ```

4. **Outputs**
   - `data/processed/crm.db` – SQLite database with all tables
   - `data/processed/features.csv` – training features
   - `data/processed/predictions.csv` – churn probabilities for a test set
   - `models/churn_model.joblib` – saved model

## What to showcase on GitHub
- Add a screenshot of a **Tableau** or **Matplotlib** dashboard showing:
  - Churn probability distribution
  - Top features (coefficients or permutation importance)
  - Segment/region churn rates
- Write a short **case study** in the README: “Actions to reduce churn based on findings.”

## Extend It
- Swap SQLite for **PostgreSQL** and connect with SQLAlchemy.
- Schedule weekly runs with **GitHub Actions** or cron.
- Add **lead scoring** or **upsell propensity** models.
- Build a simple **Streamlit** app to browse customer-level predictions.

## Notes
Data here is **synthetic** so you can publish it freely. Replace `data/raw/*.csv` with real CRM exports when you have them.
