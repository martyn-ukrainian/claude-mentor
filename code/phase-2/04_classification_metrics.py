import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import roc_auc_score, precision_score, recall_score



df = pd.read_csv("../../data/raw/WA_FN-UseC_-Telco-Customer-Churn.csv")

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna(subset=["TotalCharges"])

print(df['TotalCharges'].dtype)

X = df.drop(columns=["customerID", "Churn"])
y = (df["Churn"] == "Yes").astype(int)


numeric_cols = X.select_dtypes(include=np.number).columns
categorical_cols = X.select_dtypes(exclude=np.number).columns

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pipe = Pipeline([
  ("preprocess", ColumnTransformer([
      ("numeric", StandardScaler(), numeric_cols),
      ("categorical", OneHotEncoder(), categorical_cols),
  ])),
  ("model", LogisticRegression()),
])

pipe.fit(X_train, y_train)

y_proba_real = pipe.predict_proba(X_test)[:, 1]
y_proba_random = np.random.rand(len(y_test))

print(f"random y_proba: {y_proba_random}")

print(f"AUC real: {roc_auc_score(y_test, y_proba_real)}")
print(f"AUC random: {roc_auc_score(y_test, y_proba_random)}")

threshold = 0.2
result = (y_proba_real >= threshold).astype(int)

print(result.mean())


for threshold in [0.2, 0.3, 0.5, 0.7, 0.8]:
    y_pred_t = (y_proba_real >= threshold).astype(int)

    p = precision_score(y_test, y_pred_t)
    r = recall_score(y_test, y_pred_t)
    print(f"threshold: {threshold}, precision: {p:.3f}, recall: {r:.3f}")
