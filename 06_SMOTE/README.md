# <p align="center"> SMOTE

<p align="center"> <img src = https://dataknowsall.com/hubfs/imbalanced.png> </p>

# <p align="center"> Evaluating Imbalanced-Learn Techniques on Synthetic and Real-World Datasets

### Content

[1. Project Description](README.md#project-description)

[2. Dataset](README.md#dataset)

[3. Conclusion](README.md#conclusion)

[4. Contacts](README.md#contacts)

### Project description

This project explores various resampling techniques from the **imbalanced-learn** library ti handle class imbalance in machine learning. The study examines their impact on classification performance using both a synthetic imbalanced dataset and a real-world credit card fraud detection dataset.

[To the top](README.md#content)

### Dataset

1. **Synthetic Dataset Analysis with Decision Tree:**
    - Generated an imbalanced dataset using **make_classification()** from **sklearn.datasets**;
    - Applied multiple oversampling and undersampling techniques, including SMOTE, ADASYN, Random Oversampling, Random Undersampling, Borderline-SMOTE, Borderline-SMOTE SVM;
    - Evaluated the impact of these methods using **DecisionTreeClassifier**

2. **Credit Card Fraud Detection with Random Forest:**
    - Utilized the Kaggle credit card fraud dataset, which has a highly imbalanced distribution (fraudulent vs. non-fraudulent transactions);
    - Experimented with different resampling strategies to balance the dataset;
    - Trained **RandomForestClassifier** and assessed model performance using recall metric.

Dataset can be found using the following link: https://drive.google.com/file/d/16a8rhddapAV8nsUlPBLaR96_Kp367th6/view?usp=sharing 

[To the top](README.md#content)

### Conclusion

- Compared the effectivness of different resampling techniques in improving model performance;
- Highlighted how different resampling methods influence the decision boundary of classifiers.

[To the top](README.md#content)

### Contacts

*<p align="center">[Email](natalia_konovalova@icloud.com)</p>*

*<p align="center">[LinkedIn](https://www.linkedin.com/in/natalia-ds-198612241)</p>*

[To the top](README.md#content)