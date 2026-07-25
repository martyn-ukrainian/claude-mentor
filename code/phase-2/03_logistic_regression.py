import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
# for z in [-1, -5, -10, -50, -200]:
#     print(z, np.exp(-z))


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


z= np.array([-10, -2, -1, 0, 1, 2, 10])

# decision boundary
for z_int in z:
    print(z_int, sigmoid(z_int))



df = pd.read_csv("../../data/raw/WA_FN-UseC_-Telco-Customer-Churn.csv")



y_label = 'Churn'
print(df[y_label])

df[y_label] = df[y_label].apply(lambda x: 1 if x == 'Yes' else 0)


print(f"{y_label} type: {df[y_label].dtype}")

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors='coerce')
print(f"TotalCharges type: {df["TotalCharges"].dtype}")

print(f"TotalCharges with NaN: {df["TotalCharges"].isna().sum()}")

df = df.dropna(subset=["TotalCharges"])

print(f"TotalCharges with NaN: {df["TotalCharges"].isna().sum()}")

y_str = df.describe()
#print(y_str)


X = df.drop(columns=["customerID", "Churn"])
y = df[y_label]

numeric_cols = X.select_dtypes(include=np.number).columns
categorical_cols = X.select_dtypes(exclude=np.number).columns

print(f"Numeric columns: {numeric_cols}")
print(f"Categorical columns: {categorical_cols}")


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y )

print(f"X_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")

pipe = Pipeline([
  ("preprocess", ColumnTransformer([
      ("numeric", StandardScaler(), numeric_cols),
      ("categorical", OneHotEncoder(), categorical_cols),
  ])),
  ("model", LogisticRegression())

])

pipe.fit(X_train, y_train)


sample = X_test.iloc[:30]
X_pred = pipe.predict(sample)
X_proba = pipe.predict_proba(sample)

print("Predictions:", X_pred)
print("Probabilities:", X_proba)

model = pipe.named_steps["model"].coef_[0]

print("Model coefficients:", model)


feature_names = pipe.named_steps["preprocess"].get_feature_names_out()
coefs = pipe.named_steps["model"].coef_[0]

for name, c in zip(feature_names, coefs):
    print(f"{name}: {c}")


acc = pipe.score(X_test, y_test)

baseline = 1 - y_test.mean()
print(acc, baseline)
