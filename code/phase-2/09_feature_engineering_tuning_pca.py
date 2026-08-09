import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


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
        ("categorical", OneHotEncoder(), categorical_cols),
    ])),
    ("model", LogisticRegression(l1_ratio=1, solver="liblinear"))
])

param_grid = {
  "model__C": [0.01, 0.1, 1, 10, 100]
}

grid = GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy")
grid.fit(X_train, y_train)

print(grid.best_params_, grid.best_score_, grid.score(X_test, y_test))

print("------------ PCA -------------------")

X_numeric_scaled = StandardScaler().fit_transform(X_train[numeric_cols])

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_numeric_scaled)

print(pca.explained_variance_ratio_)


print("------------ KMeans -------------------")


kmeans = KMeans(n_clusters=3, random_state=42).fit(X_numeric_scaled)
print(kmeans.labels_)

print(f"Series \n{pd.Series(y_train.values).groupby(kmeans.labels_).mean()}")
