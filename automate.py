# 1. Drop recency_days before training
X = df.drop(columns=["customer_id", "is_churned", "recency_days"])
y = df["is_churned"]

# 2. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Train Logistic Regression
logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train, y_train)
auc_lr = roc_auc_score(y_test, logreg.predict_proba(X_test)[:,1])

# 4. Train Random Forest
rf = RandomForestClassifier(n_estimators=300, random_state=42)
rf.fit(X_train, y_train)
auc_rf = roc_auc_score(y_test, rf.predict_proba(X_test)[:,1])

# 5. Print results
print("LogReg AUC:", round(auc_lr,3))
print("RandomForest AUC:", round(auc_rf,3))
print("\nClassification Report (RF):\n", classification_report(y_test, rf.predict(X_test)))
