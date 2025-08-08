# <p align="center"> Cybersecurity Risk

<p align="center"><img src = https://www.corpnce.com/wp-content/uploads/2020/05/machine-learning.jpg></p>

## <p align="center"> Analysis and Prediction Project

## Content
[1. Project Objective](README.md#project-objective)

[2. Questions Answwered by ML Models](README.md#questions-answered-by-machine-learning-models)

[3. Dataset Description](README.md#dataset-description)

[4. Model Results and Performance Summary](README.md#model-results--performance-summary)

[5. Conclusion](README.md#conclusion)

[6. Contacts](README.md#contacts)

### Project Objective
The goal of this project is to analyze factors influencing cybersecurity risks across different businesses and to build predictive models for:
- Estimating the number of successful cybersecurity breaches (regression task)
- Predicting the security rating (classification task)
Using a dataset of 60 business samples with 10 features, the variety of machine learning models were applied, both for regression and classification, and evaluated their performance to identify the best approached for understanding and forecasting cybersecurity threats.

[To the top](README.md#content)

### Questions Answered by Machine Learning Models

|**Algorithm**|**Task Type**|**Answers the Questions**|
|--|--|--|
|Linear Regression|Regression|What continuous factors affect the number of successful breaches?|
|Decision Tree Regressor|Regression|What are the most important features and thresholds impacting breach success?|
|Random Forest Regressor|Regression|Can ensemble modeling improve the robustness of breach predictions?|
|XGBoost Regressor|Regression|Can boosting techniques improve predictive performance for breach estimation?|
|KNN Regressor|Regression|Do similar business experience similar breach patterns?|
|Support Vector Regressor|Regression|Can a non-linear capture the complex relationships in the data?|
|Logistic Regression|Classification|Can we predict if a business will receive a low, medium, or high security ratinf?|
|Decision Tree Classifier|Classification| What feature-based rules best seperate the different security rating levels?|
|Random Forest Classifier|Classification|How does an ensemble of decision trees perform on predicting security rating?|
|XGBoost Classifier|Classification|Can boosted decision trees yeild better classification performance?|
|KNN Classifier|Classification| Do business with similar profiles have the same security rating?|
|Support Vector Classifier|Classification|Can we find an optimal boundry to separate security rating categories?|

[To the top](README.md#content)

### Dataset Description 

- Samples: 60 businesses
- Features: 10 features capturing organizational, technical, and managerial aspects:

|**Feature**|**Description**|**Type**|
|--|--|--|
|Sector|Business Sector|Nominal|
|Size|Busness Size|Ordinal|
|Sec_Breach_Att|Number of security breach attemps|Scale|
|Succ_Sec_Breaches|Number of successful breach attempts|Scale|
|Security_Invest|Investment in security (thousands of USD)|Scale|
|Stock_Market|Is the business publicly traded?|Nominal|
|CEO_Gender|Gender of the CEO|Nominal|
|Sec_Rating|Security rating|Ordinal|
|CEO_Sec_Exp|CEO's cybersecurity experience|Ordinal|
|LOT_in_Business|Length of time in business (years)|Scale|

[To the top](README.md#content)

### Model Results & Performance Summary

**Regression** (Target:Number of successful breach attempts)
| Model                   | Train R² | Test R² |
|-------------------------|----------|---------|
| Linear Regression       | 0.948    | 0.846   |
| Decision Tree Regressor | 0.907    | **0.929** |
| Random Forest Regressor | 0.969    | 0.899   |
| XGBoost Regressor       | 0.989    | 0.808   |
| KNN Regressor           | 0.926    | 0.656   |
| Support Vector Regressor| **0.997**| 0.857   |

Observation:
- All regression models performed well on training data, but Decision Tree Regressor showed the best generalization on the test set.
- XGBoost, while strong on training data, may have overfitted, as suggested by a drop in test performance.

**Classification** (Target: Security Rating)
| Model                    | Train Accuracy | Test Accuracy |
|--------------------------|----------------|----------------|
| Logistic Regression      | 0.48           | 0.33           |
| Decision Tree Classifier | 0.75           | 0.25           |
| Random Forest Classifier | 0.88           | **0.58**       |
| XGBoost Classifier       | 0.98           | 0.50           |
| KNN Classifier           | 0.75           | 0.25           |
| Support Vector Classifier| 0.56           | 0.42           |

Observation:
- All classifiers suffered from overfitting due to the small dataset size.
- Random Forest Classifier demonstrated the best generalization.
- Simpler model like logistic regression underperformed, likely due to limited feature-to-class separability.

[To the top](README.md#content)

### Conclusion

This project demonstrates how various machine learning algorithms can be used to predict and analyze cybersecurity-related metrics:
- **Regression models** successfully estimated the number of successful breach attemps, with **Decision Tree Regressor** providing the most balanced performance.
- **Classification models** attempted to predict businesses' security ratings. The **Random Forest Classifier** showed the best (through still limited) generalization, highlighted the need for a larger dataset to improve classification reliability.

**Feature work**
- Expand the dataset to improve model genealization
- Explore feature engineering and oversampling for classification imbalance.
- Apply ensemble stacking or voting to boost classification performance.

[To the top](README.md#content)

### Contacts

*<p align="center">[Email](natalia_konovalova@icloud.com)</p>*

*<p align="center">[LinkedIn](https://www.linkedin.com/in/natalia-ds-198612241)</p>*

*<p align="center">[YouTube](https://www.youtube.com/@DsCsheets)</p>*

[To the top](README.md#content)