import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression



df = pd.read_csv("../../data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna(subset=["TotalCharges"])

X = df.drop(columns=["customerID", "Churn"])
y = df["Churn"]

numeric_cols = X.select_dtypes(include=np.number).columns
categorical_cols = X.select_dtypes(exclude=np.number).columns

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

preprocessor = ColumnTransformer([
    ("numeric", StandardScaler(), numeric_cols),
    ("categorical", OneHotEncoder(), categorical_cols),
])

pipe_1 = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(l1_ratio=1, solver="liblinear", C=100))
])

pipe_2 = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(l1_ratio=1, solver="liblinear", C=1))
])

pipe_3 = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(l1_ratio=1, solver="liblinear", C=0.01))
])

pipelines = [pipe_1, pipe_2, pipe_3]

count = 0

for pipe in pipelines:
    count += 1
    pipe.fit(X_train, y_train)


    train_score = pipe.score(X_train, y_train)
    test_score = pipe.score(X_test, y_test)


    model = pipe.named_steps["model"]
    # print(f"Model: {model}")

    model_coef = (model.coef_[0] == 0).sum()
    # print(f"Model coefficients: {model_coef}")


    cvs = cross_val_score(pipe, X, y, cv=5, scoring="accuracy")

    print(f"Pipe {count} ____________________________________________________________________________")
    print(f"Train score: {train_score:.4f}, Test score: {test_score:.4f}")

    print(f"Model coefficient sum: {model_coef}")

    print(f"Cross-validation scores: {cvs}")
    print(f"CV score mean: {cvs.mean():.4f}; std: {cvs.std():.4f}")


    print(f"___________________________________________________________________________________")
