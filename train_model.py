import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# =========================
# 1. LOAD DATASET
# =========================

df = pd.read_csv("data/StudentPerformanceFactors.csv")

print("Dataset loaded successfully!")
print("Rows:", len(df))
print("\nColumns:")
print(df.columns.tolist())


# =========================
# 2. SELECT FEATURES
# =========================

features = [
    "Hours_Studied",
    "Attendance",
    "Parental_Involvement",
    "Access_to_Resources",
    "Extracurricular_Activities",
    "Sleep_Hours",
    "Previous_Scores",
    "Motivation_Level",
    "Internet_Access",
    "Tutoring_Sessions",
    "Teacher_Quality",
    "Peer_Influence",
    "Physical_Activity",
    "Distance_from_Home"
]

target = "Exam_Score"

X = df[features]
y = df[target]


# =========================
# 3. FEATURE TYPES
# =========================

numeric_features = [
    "Hours_Studied",
    "Attendance",
    "Sleep_Hours",
    "Previous_Scores",
    "Tutoring_Sessions",
    "Physical_Activity"
]

categorical_features = [
    "Parental_Involvement",
    "Access_to_Resources",
    "Extracurricular_Activities",
    "Motivation_Level",
    "Internet_Access",
    "Teacher_Quality",
    "Peer_Influence",
    "Distance_from_Home"
]


# =========================
# 4. PREPROCESSING
# =========================

numeric_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        )
    ]
)

categorical_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "onehot",
            OneHotEncoder(handle_unknown="ignore")
        )
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numeric_transformer,
            numeric_features
        ),
        (
            "cat",
            categorical_transformer,
            categorical_features
        )
    ]
)


# =========================
# 5. MODEL
# =========================

model = RandomForestRegressor(
    n_estimators=400,
    random_state=42,
    max_depth=12,
    min_samples_leaf=2,
    n_jobs=-1
)


# =========================
# 6. PIPELINE
# =========================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# =========================
# 7. TRAIN / TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# =========================
# 8. TRAIN MODEL
# =========================

pipeline.fit(X_train, y_train)


# =========================
# 9. EVALUATE MODEL
# =========================

predictions = pipeline.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)

print("\nModel trained successfully!")
print(f"MAE: {mae:.2f}")
print(f"R2 Score: {r2:.3f}")



# =========================
# 10. SAVE MODEL
# =========================

joblib.dump(
    pipeline,
    "model/student_model.pkl"
)

print("\nNew model saved successfully!")
print("Path: model/student_model.pkl")