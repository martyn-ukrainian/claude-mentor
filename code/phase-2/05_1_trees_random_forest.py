import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier


df = pd.read_csv("../../data/raw/WA_FN-UseC_-Telco-Customer-Churn.csv")

print(df["TotalCharges"])

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna(subset=["TotalCharges"])

print(df["TotalCharges"])

X = df.drop(columns=["customerID", "Churn"])
y = (df["Churn"] == "Yes").astype(int)

print(X)
print(y)

numeric_cols = X.select_dtypes(include=np.number).columns
categorical_cols = X.select_dtypes(exclude=np.number).columns

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pipe = Pipeline([
  ("preprocessor", ColumnTransformer([
     ("numeric", StandardScaler(), numeric_cols),
     ("categorical", OneHotEncoder(), categorical_cols),
  ])),
  ("model", DecisionTreeClassifier())
])

pipe.fit(X_train, y_train)

acc_train = accuracy_score(y_train, pipe.predict(X_train))
acc_test = accuracy_score(y_test, pipe.predict(X_test))

print(f"Acc train: {acc_train:.3f}, acc test: {acc_test:.3f}")

tree_pipe = Pipeline([
  ("preprocessor", ColumnTransformer([
    ("numeric", StandardScaler(), numeric_cols),
    ("categorical", OneHotEncoder(), categorical_cols),
  ])),
  ("model", DecisionTreeClassifier(max_depth=4)),
])

tree_pipe.fit(X_train, y_train)
acc_tree_train = accuracy_score(y_train, tree_pipe.predict(X_train))
acc_tree_test = accuracy_score(y_test, tree_pipe.predict(X_test))
print(f"Acc tree train: {acc_tree_train:.3f}, acc tree test: {acc_tree_test:.3f}")


rf_pipe = Pipeline([
  ("preprocessor", ColumnTransformer([
    ("numeric", "passthrough", numeric_cols),
    ("categorical", OneHotEncoder(), categorical_cols),
  ])),
  ("model", RandomForestClassifier(n_estimators=200, random_state=42)),
])

rf_pipe.fit(X_train, y_train)

acc_rf_train = accuracy_score(y_train, rf_pipe.predict(X_train))
acc_rf_test = accuracy_score(y_test, rf_pipe.predict(X_test))

print(f"Acc rf train: {acc_rf_train:.3f}, acc rf test: {acc_rf_test:.3f}")


print(f"deep tree:    train {acc_train:.3f}  test {acc_test:.3f}")
print(f"shallow tree: train {acc_tree_train:.3f}  test {acc_tree_test:.3f}")
print(f"RF:           train {acc_rf_train:.3f}  test {acc_rf_test:.3f}")


rf_fi = rf_pipe.named_steps["model"].feature_importances_
print(f"RF feature importances: {rf_fi}")

rf_labels = rf_pipe.named_steps["preprocessor"].get_feature_names_out()
print(f"RF feature labels: {rf_labels}")

rf_fi_df = pd.Series(rf_fi, index=rf_labels)
print(f"RF feature importances df: \n{rf_fi_df}")


corr_martix = X_train[["tenure", "MonthlyCharges", "TotalCharges"]].corr()
print(f"Correlation matrix: \n{corr_martix}")
