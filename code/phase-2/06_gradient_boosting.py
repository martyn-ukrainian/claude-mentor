import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score


df = pd.read_csv("../../data/raw/WA_FN-UseC_-Telco-Customer-Churn.csv")

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna(subset=["TotalCharges"])

X = df.drop(columns=["customerID", "Churn"])
y = df["Churn"]

numeric_cols = X.select_dtypes(include=np.number).columns
categorical_cols = X.select_dtypes(exclude=np.number).columns


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pipe = Pipeline([
  ("preprocessor", ColumnTransformer([
    ("numeric", StandardScaler(), numeric_cols),
    ("categorical", OneHotEncoder(), categorical_cols)
  ])),
  ("gradient_boosting", GradientBoostingClassifier())
])

pipe.fit(X_train, y_train)

acc_train = accuracy_score(y_train, pipe.predict(X_train))
acc_test = accuracy_score(y_test, pipe.predict(X_test))


print(f"Train accuracy: {acc_train:.4f}")
print(f"Test accuracy: {acc_test:.4f}")



sample = X_test.iloc[:30]
y_pred = pipe.predict(sample)
y_proba = pipe.predict_proba(sample)


gradient_boosting = pipe.named_steps["gradient_boosting"].feature_importances_
names = pipe.named_steps['preprocessor'].get_feature_names_out()

print("Feature importances:")
for name, importance in sorted(zip(names, gradient_boosting), key=lambda x: x[1]):
    print(f"{name}: {importance:.4f}")
