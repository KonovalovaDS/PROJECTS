# <p align="center"> Supervised Model: Linear Regression </p>

## <p align="center"> Price prediction model for Audi vehicles </p>
<p align="center"><img src = https://media.istockphoto.com/id/1181190845/photo/audi-s5-in-motion.jpg?s=612x612&w=0&k=20&c=biQ4ZQmskFVXbLubSx_NYA-2yz8MUTTYOtUoT33PM5I=></p>

## Content
[1. Project description](README.md#project-description)

[2. Dataset](README.md#dataset)

[3. Technologies](README.md#technologies)

[4. Contacts](README.md#contacts)

## Project description
The main target is to create ML-model which would predict the proces for Audi vehicles. The Mean Absolute Error (MAE) shall not exceed 2.000 USD.

Additional metrics such as $R^2$ and MAPE have been also calculated.

The second target is to investigate how the different methods of outliers calculation influence on the result of the ML-model.

The following best results have been achieved:

| Metrics | Train | Test |
|:---|---:|---:|
| $R^2$ | 0.927 | 0.926 |
| MAE | 1886.559 | 1869.705 |
| MAPE | 8.647 | 8.612 |

[To the top](README.md#content)

## Dataset

Each vehicle is described with the following features:

- model - model of the vehicle

- year - year of maufacturing

- price - price (**target feature**)

- transmission - transmission (manual, automatic, semiautomatic)

- mileage - mileage

- fuelType - engine type (petrol, diesel, hybrid)

- tax - tax

- mpg - fuel consumption

- engineSize - engine size

Additionl features have been created, few gaps have been filled. Categorical features have been encoded using OrdinalEncoding & OneHotEncoding

[To the top](README.md#content)

## Technologies
The following techniques have been used:

1. Z-score method

2. Method Tukey

3. SelectKBest

4. RobustScaler, PowerTransformer & QuantileTransformer for normalization

[To the top](README.md#content)

## Contacts

Email: natalia_konovalova@icloud.com

Kaggle: https://www.kaggle.com/nataliamantyk 

LinkedIn: https://www.linkedin.com/in/natalia-ds-198612241

[To the top](README.md#content)


