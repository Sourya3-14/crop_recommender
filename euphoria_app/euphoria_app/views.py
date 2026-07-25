from django.shortcuts import render
from django.conf import settings
from .forms import CropPredictionForm
import joblib
import os
import time

# Image/model processing
from PIL import Image
import numpy as np
try:
    from tensorflow.keras.models import load_model
except Exception:
    # If tensorflow not available at import time, we'll handle when used
    load_model = None
import json
import re
import ast


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

# Plant disease recognition model
DISEASE_MODEL_PATH = os.path.join(settings.BASE_DIR, "ml", "plant_disease_recog_model_pwp.keras")
disease_model = None
if load_model is not None:
    try:
        disease_model = load_model(DISEASE_MODEL_PATH)
    except Exception as _:
        # keep disease_model as None if loading fails
        disease_model = None


def _load_disease_labels():
    """Try to load human-readable class labels for the disease model.

    Priority:
    1. `ml/disease_labels.txt` — one label per line
    2. Extract a literal `class_names = [...]` list from the training notebook
       `notebook/Plant_Disease_Model_Training.ipynb` if present.
    Returns a list of labels or None.
    """
    # 1) labels file
    labels_path = os.path.join(settings.BASE_DIR, "ml", "class_names.txt")
    if os.path.exists(labels_path):
        try:
            with open(labels_path, "r", encoding="utf-8") as fh:
                labels = [line.strip() for line in fh.readlines() if line.strip()]
                if labels:
                    return labels
        except Exception:
            pass

    # 2) try to extract from training notebook
    nb_path = os.path.join(settings.BASE_DIR, "notebook", "Plant_Disease_Model_Training.ipynb")
    if os.path.exists(nb_path):
        try:
            with open(nb_path, "r", encoding="utf-8") as fh:
                nb = json.load(fh)

            for cell in nb.get("cells", []):
                if cell.get("cell_type") != "code":
                    continue
                src = "".join(cell.get("source", []))
                # look for a literal list assigned to class_names
                m = re.search(r"class_names\s*=\s*(\[.*?\])", src, re.S)
                if m:
                    try:
                        labels = ast.literal_eval(m.group(1))
                        if isinstance(labels, (list, tuple)) and labels:
                            return [str(x) for x in labels]
                    except Exception:
                        continue
        except Exception:
            pass

    return None


# cache labels on module load
DISEASE_LABELS = _load_disease_labels()

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


def disease_detect(request):
    """
    Handle image upload and run the plant disease recognition Keras model.
    Renders the same `website/predict.html` template and adds
    `disease_result`, `disease_image_path`, and `disease_confidence` to context.
    """
    disease_result = None
    disease_image_path = None
    disease_confidence = None

    if request.method == "POST" and "disease_image" in request.FILES:
        uploaded = request.FILES.get("disease_image")

        if disease_model is None:
            disease_result = "Disease model not available on server."
        else:
            try:
                img = Image.open(uploaded).convert("RGB")
                # Determine target size from model input when possible.
                target_size = (160, 160)
                try:
                    input_shape = getattr(disease_model, 'input_shape', None)
                    if input_shape:
                        # input_shape can be (None, H, W, C) or (H, W, C) or (None, C, H, W)
                        if len(input_shape) == 4:
                            _, h, w, _ = input_shape
                            if h and w:
                                target_size = (int(w), int(h))
                        elif len(input_shape) == 3:
                            h, w, _ = input_shape
                            target_size = (int(w), int(h))
                except Exception:
                    target_size = (160, 160)

                img_resized = img.resize(target_size)
                x = np.asarray(img_resized, dtype=np.float32) / 255.0
                x = np.expand_dims(x, 0)

                preds = disease_model.predict(x)
                # preds may be probabilities per-class
                class_idx = int(np.argmax(preds[0]))
                confidence = float(np.max(preds[0]))

                # Map index to human-readable label when possible
                if DISEASE_LABELS and 0 <= class_idx < len(DISEASE_LABELS):
                    disease_result = DISEASE_LABELS[class_idx]
                else:
                    disease_result = f"Class {class_idx}"
                disease_confidence = round(confidence * 100, 2)

                # Save uploaded image into static/images/analysis for display
                save_dir = os.path.join(settings.BASE_DIR, "static", "images", "analysis")
                os.makedirs(save_dir, exist_ok=True)
                filename = f"upload_{int(time.time())}.jpg"
                save_path = os.path.join(save_dir, filename)
                img.save(save_path)
                disease_image_path = f"images/analysis/{filename}"

            except Exception as exc:
                disease_result = f"Error processing image: {exc}"

    # include the crop prediction form so the page renders both features
    try:
        form = CropPredictionForm()
    except Exception:
        form = None

    return render(request, "website/predict.html", {
        "form": form,
        "disease_result": disease_result,
        "disease_image_path": disease_image_path,
        "disease_confidence": disease_confidence,
    })