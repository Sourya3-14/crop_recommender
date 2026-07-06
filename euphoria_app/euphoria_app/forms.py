from django import forms

class CropPredictionForm(forms.Form):
    nitrogen = forms.FloatField(
        min_value=0,
        max_value=140,
        error_messages={
            "min_value": "Nitrogen cannot be negative",
            "max_value": "Nitrogen should not exceed 140"
        }
    )

    phosphorus = forms.FloatField(
        min_value=5,
        max_value=150,
        error_messages={
            "min_value": "Phosphorus must be at least 5",
            "max_value": "Phosphorus should not exceed 150"
        }
    )

    potassium = forms.FloatField(
        min_value=5,
        max_value=210,
        error_messages={
            "min_value": "Potassium must be at least 5",
            "max_value": "Potassium should not exceed 210"
        }
    )

    temperature = forms.FloatField(
        min_value=0,
        max_value=50,
        error_messages={
            "min_value": "below 0°C farming is not possible",
            "max_value": "above 50°C farming is not possible"
        }
    )

    humidity = forms.FloatField(
        min_value=0,
        max_value=100,
        error_messages={
            "min_value": "Humidity can not be nagative",
            "max_value": "Humidity cannot exceed 100%"
        }
    )

    ph = forms.FloatField(
        min_value=0,
        max_value=14,
        error_messages={
            "min_value": "pH cannot be negative",
            "max_value": "pH must be between 0 and 14"
        }
    )

    rainfall = forms.FloatField(
        min_value=0,
        max_value=4000,
        error_messages={
            "min_value": "Rainfall can not be negative",
            "max_value": "Rainfall is above possible range"
        }
    )