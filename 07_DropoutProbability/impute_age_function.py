import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

def impute_age(df, return_pipeline = False):
    features = ['gender', 'education_level', 'employment_status', 'industry', 'course_category',
                'engagement_score', 'progress_percent', 'assignment_submission_rate', 'attendance_rate',
                'satisfaction_rating']
    
    categorical_features = ['gender', 'education_level', 'employment_status', 'industry', 'course_category']
    numerical_features = ['engagement_score', 'progress_percent', 'assignment_submission_rate', 'attendance_rate', 'satisfaction_rating']
    
    df_known = df[df['age'].notna()].copy()
    df_unknown = df[df['age'].isna()].copy()
    
    X_known = df_known[features]
    y_known = df_known['age']
    X_unknown = df_unknown[features]
    
    preprocessor = ColumnTransformer([
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy = 'median')),
            ('scaler', StandardScaler())]), numerical_features),
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy = 'most_frequent')),
            ('encoder', OneHotEncoder(handle_unknown = 'ignore'))]), categorical_features)])
    
    pipeline = Pipeline([
        ('preprocessing', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators = 100, random_state = 42))])
    pipeline.fit(X_known, y_known)
    predicted_age = pipeline.predict(X_unknown).round().astype(int)
    
    df.loc[df['age'].isna(), 'age'] = predicted_age
    
    if return_pipeline:
        return df, pipeline
    
    return df
