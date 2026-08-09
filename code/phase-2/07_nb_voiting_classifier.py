import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import VotingClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB, BernoulliNB

df = pd.read_csv("../../data/raw/WA_FN-UseC_-Telco-Customer-Churn.csv")

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors='coerce')
df = df.dropna(subset=["TotalCharges"])

X = df.drop(columns=["customerID", "Churn"])
y = (df["Churn"] == "Yes").astype(int)

numeric_cols = X.select_dtypes(include=np.number).columns
categorical_cols = X.select_dtypes(exclude=np.number).columns

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pipe_gnb = Pipeline([
    ("preprocessor", ColumnTransformer([
        ("numeric", StandardScaler(), numeric_cols),
    ])),
    ("model", GaussianNB())
])

pipe_bnb = Pipeline([
    ("preprocessor", ColumnTransformer([
        ("categorical", OneHotEncoder(), categorical_cols)
    ])),
    ("model", BernoulliNB())
])

combined = VotingClassifier(
  estimators=[("gnb", pipe_gnb), ("bnb", pipe_bnb)],
  voting="soft"
)

combined.fit(X_train, y_train)
acc_train = accuracy_score(y_train, combined.predict(X_train))
acc_test = accuracy_score(y_test, combined.predict(X_test))

print(f"Accuracy (train): {acc_train}")
print(f"Accuracy (test): {acc_test}")
