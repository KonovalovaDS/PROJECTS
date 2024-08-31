# <p align="center"> New York City

<p align="center"> <img src = https://s.abcnews.com/images/Business/nyc-taxis-gty-rc-200220_hpMain.jpg> </p>

# <p align="center"> Taxi Trip Duration Prediction

### Content

[1. Project description](README.md#project-description)

[2. Dataset](README.md#dataset)

[3. Conclusion](README.md#conclusion)

[4. Contacts](README.md#contacts)

### Project description

**Business Goal**:
Define the features and use them to predict the duration of a taxi trip

**Technical Task**:
Build a machine learning model, that based on the proposed features, will predict a numerical feature - taxi ride time, that is, solve a regression problem.

**Main steps**:
1. Create the data set based on multiple sources of information;
2. Create new features and idetify the most significant ones to be used during the modeling;
3. Explore the provided data and identify the patterns;
4. Build several models and select the one that shows the best result for a given metric;
5. Design a process for predicting trip duration for the new data.

[To the top](README.md#content)

### Dataset

All used data set can be found in the folder "DATA"(https://drive.google.com/drive/folders/1NRC8dqhSmrQ1_AglqV15JTVkqoPBusch?usp=sharing). The following additional information has been used:
- Public Holidays;
- Weather conditions information;
<<<<<<< HEAD
- Open Source Routing Machine (OSRM) data.
=======
- Open Source Routing Machine (OSRM) data
>>>>>>> a01b4bba436852b2901de67048ff019dc5ef81f6

[To the top](README.md#content)

### Conclusion

The best results have been reached with XGBoosting algorithm. The metric to avalute the results: Root Mean Squared Log Error (RMSLE)
$$RMSLE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (log (y_i + 1) - log (\hat{y}_i + 1))^2}$$


|**Model**|**RMSLE on train**|**RMSLE on valid**|
|:--|:--|:--|
|Linear Regression|0.534|0.536|
|Linear Regression on Polynomial Features|0.467|0.613|
|Linear Regression $L^2$-Regularization|0.469|0.475|
|Decision Tree|0.406|0.430|
|Random Forest Regressor|0.399|0.393|
|Gradient Boosting|0.372|0.393|
|XGBoost|--|0.393|

[To the top](README.md#content)

### Contacts

*<p align="center">[Email](natalia_konovalova@icloud.com)</p>*

*<p align="center">[Kaggle](https://www.kaggle.com/nataliamantyk)</p>* 

*<p align="center">[LinkedIn](https://www.linkedin.com/in/natalia-ds-198612241)</p>*

[To the top](README.md#content)
