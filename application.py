from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application=Flask(__name__)

app=application

## Route for a home page 

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        # Print all form inputs to debug
        print("Form Input:", request.form)

        # Safely get scores and check for None
        reading_score_raw = request.form.get('reading-score')
        writing_score_raw = request.form.get('writing-score')

        print("Raw Reading Score:", reading_score_raw)
        print("Raw Writing Score:", writing_score_raw)

        try:
            reading_score = float(reading_score_raw)
            writing_score = float(writing_score_raw)
        except (TypeError, ValueError) as e:
            print("Error converting scores to float:", e)
            return render_template('home.html', results="Invalid score input!")

        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('race_ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=reading_score,
            writing_score=writing_score
        )

        pred_df = data.get_data_as_data_frame()
        print("Prediction DataFrame:\n", pred_df)

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        return render_template('home.html', results=results[0])


if __name__ == "__main__":
    app.run(host="0.0.0.0")