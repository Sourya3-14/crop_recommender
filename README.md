# Crop Recommendation Project

SmartCrop is a full-stack web application for crop recommendation. It combines a Django-based web interface with a machine learning model built in a Jupyter notebook to predict suitable crops based on soil and climate input values.

**[Live Application Link](http://13.207.72.59:8000/)**

## Project Overview

This project includes:

- A Django web application for user interaction and prediction
- A crop recommendation form that accepts soil and weather-related inputs
- A trained machine learning model that predicts the most suitable crop
- A Jupyter notebook containing the data analysis, preprocessing, model training, and model export workflow

## Features

- Home, about, contact, team, and analysis pages
- Crop prediction form with input validation
- Model-based crop recommendation using soil and climatic features
- Image-based result display for the predicted crop
- Responsive website design with Django templates

## Project Structure

- [euphoria_app/](euphoria_app/) - Django project folder
  - [euphoria_app/euphoria_app/](euphoria_app/euphoria_app/) - Django app configuration, views, URLs, and forms
  - [euphoria_app/ml/](euphoria_app/ml/) - Saved model artifacts
  - [euphoria_app/templates/](euphoria_app/templates/) - HTML templates for the website
- [notebook/crop_recommender.ipynb](notebook/crop_recommender.ipynb) - Jupyter notebook for model development

## Machine Learning Notebook

The notebook in [notebook/crop_recommender.ipynb](notebook/crop_recommender.ipynb) contains:

- Data loading and exploration
- Visualization of crop-related features
- Data preprocessing and label encoding
- Model training for crop classification
- Model serialization into pickle files used by the Django app

The trained model files used by the app are:

- [euphoria_app/ml/crop_model_nb.pkl](euphoria_app/ml/crop_model_nb.pkl)
- [euphoria_app/ml/label_encoder.pkl](euphoria_app/ml/label_encoder.pkl)

## Tech Stack

- Python
- Django
- scikit-learn
- pandas
- numpy
- joblib
- Jupyter Notebook
- HTML/CSS

## Prerequisites

Make sure you have the following installed:

- Python 3.12 or newer
- pip
- virtual environment support

## Installation

1. Clone the repository

   ```bash
   git clone <repository-url>
   cd euphoria
   ```

2. Create and activate a virtual environment

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies

   ```bash
   cd euphoria_app
   pip install -r requirements.txt
   ```

## Running the Application

Start the development server:

```bash
cd euphoria_app
python manage.py runserver
```

Then open your browser and visit :

- http://127.0.0.1:8000/

## Running Using docker

run the folloing commands and visit : http://127.0.0.1:8000/

```
docker pull attention824/crop_recommender

docker run --name crop_app -p 8000:8000 attention824/crop_recommender
```

## Using the App

- Visit the home page to explore the website
- Analysys page contains the details about the ml models
- Open the prediction page to enter soil and climate data
- Submit the form to receive a recommended crop prediction

## License

This project is intended for educational and demonstration purposes.
