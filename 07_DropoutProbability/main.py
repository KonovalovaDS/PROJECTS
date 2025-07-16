from fastapi import FastAPI
from pydantic import BaseModel
import dill
import numpy as np

app = FastAPI(title = 'Student Dropout Probability Predictor')

with open('rf_reg_final.pkl', 'rb') as f:
    model = dill.load(f)
    
class StudentInput(BaseModel):
    engagement_score: float
    engagement_satisfaction: float
    participation_level: float
    progress_percent: float
    attendance_rate: float
    progress_satisfaction: float
    participation_satisfaction: float
    active_days: int
    course_fee: float
    
@app.get('/')
def root():
    return {'message' : 'Welcome to the Dropout Predictor API!'}

@app.post('/predict')
def predict_dropout(input_data: StudentInput):
    input_array = np.array([[v for v in input_data.model_dump().values()]])
    prediction = model.predict(input_array)[0]
    return {
        'dropout_probability' : round(float(prediction), 4),
        'message' : 'Prediction completed successfully.'
    }
     