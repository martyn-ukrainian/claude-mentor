import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB, BernoulliNB

df = pd.read_csv("../../data/raw/WA_FN-UseC_-Telco-Customer-Churn.csv")

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna(subset=["TotalCharges"])

X = df.drop(columns=["customerID", "Churn"])
y = (df["Churn"] == "Yes").astype(int)

numertic_cols = X.select_dtypes(include=np.number).columns
categorical_cols = X.select_dtypes(exclude=np.number).columns

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pipe_knn = Pipeline([
  ("preprocessor", ColumnTransformer([
    ("number", StandardScaler(), numertic_cols),
    ("category", OneHotEncoder(), categorical_cols)
  ])),
  ("model", KNeighborsClassifier())
])

pipe_svc = Pipeline([
  ("preprocessor", ColumnTransformer([
    ("number", StandardScaler(), numertic_cols),
    ("category", OneHotEncoder(), categorical_cols)
  ])),
  ("model", SVC())
])

pipe_nb = Pipeline([
  ("preprocessor", ColumnTransformer([
    ("number", StandardScaler(), numertic_cols),
    ("category", OneHotEncoder(), categorical_cols)
  ])),
  ("model", GaussianNB())
])

pipe_knn.fit(X_train, y_train)
pipe_svc.fit(X_train, y_train)
pipe_nb.fit(X_train, y_train)

acc_train_pipe_knn = accuracy_score(y_train, pipe_knn.predict(X_train))
acc_train_pipe_svc = accuracy_score(y_train, pipe_svc.predict(X_train))
acc_train_pipe_nb = accuracy_score(y_train, pipe_nb.predict(X_train))

acc_test_pipe_knn = accuracy_score(y_test, pipe_knn.predict(X_test))
acc_test_pipe_svc = accuracy_score(y_test, pipe_svc.predict(X_test))
acc_test_pipe_nb = accuracy_score(y_test, pipe_nb.predict(X_test))

print(f"KNN:          train {acc_train_pipe_knn:.3f}  test {acc_test_pipe_knn:.3f}")
print(f"SVM:          train {acc_train_pipe_svc:.3f}  test {acc_test_pipe_svc:.3f}")
print(f"Naive Bayes:  train {acc_train_pipe_nb:.3f}  test {acc_test_pipe_nb:.3f}")

pipe_nb_only_number = Pipeline([
  ("preprocessor", ColumnTransformer([
    ("number", StandardScaler(), numertic_cols),
  ])),
  ("model", GaussianNB())
])


pipe_nb_only_number.fit(X_train, y_train)

acc_train_pipe_nb_only_number = accuracy_score(y_train, pipe_nb_only_number.predict(X_train))
acc_test_pipe_nb_only_number = accuracy_score(y_test, pipe_nb_only_number.predict(X_test))

print(f"Naive Bayes (only number): train {acc_train_pipe_nb_only_number:.3f}  test {acc_test_pipe_nb_only_number:.3f}")

pipe_bnb = Pipeline([
  ("preprocessor", ColumnTransformer([
    ("number", StandardScaler(), numertic_cols),
    ("category", OneHotEncoder(), categorical_cols)
  ])),
  ("model", BernoulliNB())
])

pipe_bnb.fit(X_train, y_train)

acc_train_pipe_bnb = accuracy_score(y_train, pipe_bnb.predict(X_train))
acc_test_pipe_bnb = accuracy_score(y_test, pipe_bnb.predict(X_test))

print(f"Bernoulli NB: train {acc_train_pipe_bnb:.3f}  test {acc_test_pipe_bnb:.3f}")
