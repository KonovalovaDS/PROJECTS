# <p align="center"> Online Learning

<p align="center"><img src = https://www.workplacelanguages.com/wp-content/uploads/2020/08/Online-Courses.jpg></p>

## <p align = "center"> Students Dropout Probability Prediction

## Content
[1. Project Description](README.md#project-description)

[2. Dataset](README.md#dataset) 

[3. Model Deployment](README.md#model-deployment)

[4. Conclusion](README.md#conclusion)

[5. Contacts](README.md#contacts)

### Project Description
In the fast-growing EdTech sector, one of the primary challenges faced by online learning platforms is student retention. With a large volume of courses available, students may begin their journey in an online course but fail to complete it due to various reasons such as lack of engagement, difficulty in course content, poor course experiences, or personal issues. Predicting which students are at risk of leaving a course can help EdTech companies take proactive steps to improve student engagement, adjust course materials, or offer personalized support.

By developing a model that predicts the likelihood of student drop-off, this project addresses the problem of student disengagement and provides a framework for increasing student retention and course completion rates.

[To the top](README.md#content)

### Dataset

The dataset can be found following the link: https://www.kaggle.com/datasets/vandanrana/student-drop-off-prediction-in-edtech-courses

The dataset contains 40,000 records and 22 features, representing demographic, behavioral, and course-related characteristics. Key feature categories include:

- **Demographic**: age, gender, country, state, education level, employment status, industry, years of experience
- **Course Info**: course name, course category, course fee, enrollment date, last active date
- **Engagement & Performance**: engagement score, progress percent, assignment submission rate, attendance rate, satisfaction rating
- **Identifiers**: student id, student name
- **Target Variable**: dropout probability (continuous value indicating likelihood of dropping out)

[To the top](README.md#content)

### Model Deployment

- **Model**: Random Forest Regressor optimized with cross-validation and hyperparameters tuning. Missing values imputation with trained regressors / classifiers, feature encoding, statistical analysis.

- **Deployment**: FastAPI + Docker for web-based access.

- **Build the Docker Image** 

docker build -t dropout-api .

- **Run the API**

docker run -p 8000:8000 dropout-api

- **Open in Browser**

http://127.0.0.1:8000/docs

- **Example Input**

{
  "engagement_score": 0.7,
  "engagement_satisfaction": 0.6,
  "participation_level": 0.9,
  "progress_percent": 0.85,
  "attendance_rate": 0.8,
  "progress_satisfaction": 0.75,
  "participation_satisfaction": 0.65,
  "active_days": 42,
  "course_fee": 500.0
}

- **Example Response**

{
  "dropout_probability": 0.2821,
  "message": "Prediction completed successfully."
}

The model uses .pkl files for saved pipelines and final predictors. Deployment does **not** require any Python setup for the user - just broweser / API access.

[To the top](README.md#content)

### Conclusion

1. **Feature Selection**: Nine MI-selected features are as good as the full feature set. This improves model interpretability without sacrificing performance.

2. **Model Choice**: Random Forest outperforms Linear Regression in every aspect - this is expected, especially for nonlinear relationships. Since dropout behavior is likely influenced by nonlinear and interaction effects, tree-based methods are more suitable.

3. **Baseline Models**: The results provide an excellent starting benchmark. Random Forest with nine features is the best compact model in terms of performance and simplicity.

4. **Simulating Real-World Performance**: MAE: 0.004, RMSE: 0.000 between actual dropout and predicted dropout on the actual dataset. This indicates excellent predictive performance of the model on known data, which almost negligible error. By using multivariate normal sampling from the empirical covariance matrix of real data, the simulated samples preserve the real-world relationships between features.  

[To the top](README.md#content)

### Contacts

*<p align="center">[Email](natalia_konovalova@icloud.com)</p>*

*<p align="center">[LinkedIn](https://www.linkedin.com/in/natalia-ds-198612241)</p>*

*<p align="center">[YouTube](https://www.youtube.com/@DsCsheets)</p>*

[To the top](README.md#content)