
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import joblib
from pathlib import Path

def main(in_csv='data/processed/features.csv'):
    df = pd.read_csv(in_csv)
    X = df.drop(columns=['customer_id','is_churned'])
    y = df['is_churned']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Baseline: Logistic Regression
    logreg = LogisticRegression(max_iter=1000)
    logreg.fit(X_train, y_train)
    y_pred_lr = logreg.predict(X_test)
    y_proba_lr = logreg.predict_proba(X_test)[:,1]
    auc_lr = roc_auc_score(y_test, y_proba_lr)

    # Random Forest
    rf = RandomForestClassifier(n_estimators=300, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    y_proba_rf = rf.predict_proba(X_test)[:,1]
    auc_rf = roc_auc_score(y_test, y_proba_rf)

    print('LogReg AUC:', round(auc_lr,3))
    print('RandomForest AUC:', round(auc_rf,3))
    print('\nClassification Report (RF):\n', classification_report(y_test, y_pred_rf))

    # Save best model (pick RF if better)
    model = rf if auc_rf >= auc_lr else logreg
    Path('models').mkdir(exist_ok=True)
    joblib.dump(model, 'models/churn_model.joblib')

    # Save predictions
    df_test = df.iloc[X_test.index][['customer_id']].copy()
    df_test['churn_probability'] = y_proba_rf if model is rf else y_proba_lr
    out_path = 'data/processed/predictions.csv'
    df_test.to_csv(out_path, index=False)
    print('Saved model and predictions to', out_path)

if __name__ == '__main__':
    main()
