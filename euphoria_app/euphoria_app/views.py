from django.shortcuts import render
from django.conf import settings
from .forms import CropPredictionForm
import joblib
import os


MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "ml",
    "crop_model_nb.pkl"
)
LABEL_ENCODER_PATH = os.path.join(
    settings.BASE_DIR,
    "ml",
    "label_encoder.pkl"
)

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)

def home(request):
    return render(request, "website/home.html")


def about(request):
    return render(request, "website/about.html")


def contact(request):
    return render(request, "website/contact.html")


def team(request):
    return render(request, "website/team.html")


def analysis(request):
    return render(request, "website/analysis.html")


def predict(request):
    prediction = None
    crop_name = None
    crop_image_path = None

    if request.method == "POST":
        form = CropPredictionForm(request.POST)

        if form.is_valid():
            data = [
                [
                    form.cleaned_data["nitrogen"],
                    form.cleaned_data["phosphorus"],
                    form.cleaned_data["potassium"],
                    form.cleaned_data["temperature"],
                    form.cleaned_data["humidity"],
                    form.cleaned_data["ph"],
                    form.cleaned_data["rainfall"],
                ]
            ]

            prediction = model.predict(data)[0]
            raw_crop_name = label_encoder.inverse_transform([prediction])[0]
            
            # Clean up potential leading/trailing whitespace from the encoder output
            crop_name = raw_crop_name.strip()
            
            # Create a safe file string path based on lowercase name (e.g., "rice.jpg")
            crop_image_path = f"images/crops/{crop_name.lower()}.jpg"

    else:
        form = CropPredictionForm()

    return render(
        request,
        "website/predict.html",
        {
            "form": form,
            "prediction": crop_name,
            "crop_image_path": crop_image_path,
        },
    )