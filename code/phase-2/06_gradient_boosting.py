import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression


df = pd.read_csv("../../data/raw/WA_FN-UseC_-Telco-Customer-Churn.csv")

df["TotalCharges"] = df.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna(subset=["TotalCharges"])

X = df.drop(columns=["customerID", "Churn"])
y = df["Churn"]

numeric_cols = X.select_dtypes(includes=np.number).columns
categorical_cols = X.select_dtypes(excludes=np.number).columns


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pipe = Pipeline([
  ("preprocessor", ColumnTransformer([
    ("numeric", StandardScaler(), numeric_cols),
    ("categorical", OneHotEncoder(), categorical_cols)
  ])),
  ("model", LogisticRegression())
])

pipe.fit(X_train, y_train)

sample = y_test.iloc[:30]
y_pred = pipe.predict(sample)
y_proba = pipe.predict_proba(sample)

loss = -(y_proba * np.log(y_pred) + (1 - y_proba) * np.log(1 - y_pred))
