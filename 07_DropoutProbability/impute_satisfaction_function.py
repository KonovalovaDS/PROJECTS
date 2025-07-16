import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

def impute_satisfaction_rating(df, return_pipeline = False):
    features = ['engagement_score', 'attendance_rate', 'assignment_submission_rate',
                'progress_percent', 'course_category']
    
    categorical_features = ['course_category']
    numerical_features = ['engagement_score', 'attendance_rate', 'assignment_submission_rate', 'progress_percent']
    
    df_known = df[df['satisfaction_rating'].notna()].copy()
    df_unknown = df[df['satisfaction_rating'].isna()].copy()
    
    X_known = df_known[features]
    y_known = df_known['satisfaction_rating']
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
    predicted_satisfaction_rating = pipeline.predict(X_unknown)
    
    df.loc[df['satisfaction_rating'].isna(), 'satisfaction_rating'] = predicted_satisfaction_rating
    
    # add missing indicator
    df['satisfaction_rating_missing'] = df['satisfaction_rating'].isna().astype(int)
    if return_pipeline:
        return df, pipeline
    return df