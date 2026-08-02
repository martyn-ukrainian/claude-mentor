import pandas as pd
import numpy as np

from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier


df = pd.read_csv("../../data/raw/WA_FN-UseC_-Telco-Customer-Churn.csv")

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna(subset=["TotalCharges"])

X = df.drop(columns=["customerID", "Churn"])
y = (df["Churn"] == "Yes").astype(int)

numeric_cols = X.select_dtypes(include=np.number).columns
categorical_cols = X.select_dtypes(exclude=np.number).columns

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


pipe = Pipeline([
  ("preprocessor", ColumnTransformer([
    ("numeric", StandardScaler(), numeric_cols),
    ("categorical", OneHotEncoder(), categorical_cols)
  ])),
  ("deep_tree", DecisionTreeClassifier(random_state=42))
])


pipe.fit(X_train, y_train)

train_acc = accuracy_score(y_train, pipe.predict(X_train))
test_acc = accuracy_score(y_test, pipe.predict(X_test))

print(f"train acc: {train_acc:.3f}, test acc: {test_acc:.3f}")

shallow_pipe = Pipeline([
  ("preprocessor", ColumnTransformer([
    ("numeric", StandardScaler(), numeric_cols),
    ("categorical", OneHotEncoder(), categorical_cols)
  ])),
  ("shallow_tree", DecisionTreeClassifier(max_depth=4, random_state=42))
])

shallow_pipe.fit(X_train, y_train)

shallow_train_acc = accuracy_score(y_train, shallow_pipe.predict(X_train))
shallow_test_acc = accuracy_score(y_test, shallow_pipe.predict(X_test))

print(f"shallow train acc: {shallow_train_acc:.3f}, shallow test acc: {shallow_test_acc:.3f}")

rf_pipe = Pipeline([
  ("preprocessor", ColumnTransformer([
    ("numeric", StandardScaler(), numeric_cols),
    ("categorical", OneHotEncoder(), categorical_cols)
  ])),
  ("rf", RandomForestClassifier(n_estimators=200, random_state=42))
])

rf_pipe.fit(X_train, y_train)

rf_train_acc = accuracy_score(y_train, rf_pipe.predict(X_train))
rf_test_acc = accuracy_score(y_test, rf_pipe.predict(X_test))

print(f"rf train acc: {rf_train_acc:.3f}, rf test acc: {rf_test_acc:.3f}")


importances = pd.Series(
  rf_pipe.named_steps["rf"].feature_importances_,
  index=rf_pipe.named_steps["preprocessor"].get_feature_names_out()
).sort_values(ascending=False)

print(importances.head(10))

print(X_train[["tenure", "MonthlyCharges", "TotalCharges"]].corr())
