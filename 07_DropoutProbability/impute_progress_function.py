import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

def impute_progress_percent(df, return_pipeline = False):
    features = ['engagement_score', 'attendance_rate', 'assignment_submission_rate',
                'education_level', 'employment_status', 'satisfaction_rating']
    
    categorical_features = ['education_level', 'employment_status']
    numerical_features = ['engagement_score', 'attendance_rate', 'assignment_submission_rate',
                          'satisfaction_rating']
    
    df_known = df[df['progress_percent'].notna()].copy()
    df_unknown = df[df['progress_percent'].isna()].copy()
    
    X_known = df_known[features]
    y_known = df_known['progress_percent']
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
    predicted_progress_percent = pipeline.predict(X_unknown)
    
    df.loc[df['progress_percent'].isna(), 'progress_percent'] = predicted_progress_percent
    
    # add missing indicator
    df['progress_percent_missing'] = df['progress_percent'].isna().astype(int)
    if return_pipeline:
        return df, pipeline
    return df
