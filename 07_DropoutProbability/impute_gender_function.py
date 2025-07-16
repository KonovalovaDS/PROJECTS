import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

def impute_gender(df, return_pipeline = False):
    features = [
        'age', 'education_level', 'employment_status', 'industry', 
        'course_category', 'engagement_score', 'progress_percent', 
        'assignment_submission_rate', 'attendance_rate', 'satisfaction_rating'
    ]

    categorical_features = ['education_level', 'employment_status', 'industry', 'course_category']
    numerical_features = ['age', 'engagement_score', 'progress_percent', 'assignment_submission_rate', 'attendance_rate', 'satisfaction_rating']

    df_known = df[df['gender'].notna()].copy()
    df_unknown = df[df['gender'].isna()].copy()

    X_known = df_known[features]
    y_known = df_known['gender']
    X_unknown = df_unknown[features]

    preprocessor = ColumnTransformer([
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), numerical_features),
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(handle_unknown='ignore'))
        ]), categorical_features)
    ])

    pipeline = Pipeline([
        ('preprocessing', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    pipeline.fit(X_known, y_known)
    predicted_gender = pipeline.predict(X_unknown)

    df.loc[df['gender'].isna(), 'gender'] = predicted_gender
    if return_pipeline:
        return df, pipeline
    return df