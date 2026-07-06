from .forms import CropPredictionForm
from django.test import TestCase
from django.urls import reverse


class CropPredictionFormTest(TestCase):

    def test_valid_form(self):
        form = CropPredictionForm(data={
            "nitrogen": 90,
            "phosphorus": 40,
            "potassium": 43,
            "temperature": 20,
            "humidity": 80,
            "ph": 6.5,
            "rainfall": 200
        })

        self.assertTrue(form.is_valid())

    def test_invalid_nitrogen(self):
        form = CropPredictionForm(data={
            "nitrogen": -5,
            "phosphorus": 40,
            "potassium": 43,
            "temperature": 20,
            "humidity": 80,
            "ph": 6.5,
            "rainfall": 200
        })

        self.assertFalse(form.is_valid())

class PredictionViewTest(TestCase):

    def test_prediction(self):

        response = self.client.post(
            reverse("predict"),
            {
                "nitrogen": 90,
                "phosphorus": 40,
                "potassium": 43,
                "temperature": 20,
                "humidity": 80,
                "ph": 6.5,
                "rainfall": 200
            }
        )

        self.assertEqual(response.status_code, 200)

class ViewTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_about_page_loads(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_loads(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_team_page_loads(self):
        response = self.client.get(reverse("team"))
        self.assertEqual(response.status_code, 200)

    def test_analysis_page_loads(self):
        response = self.client.get(reverse("analysis"))
        self.assertEqual(response.status_code, 200)

    def test_predict_page_loads(self):
        response = self.client.get(reverse("predict"))
        self.assertEqual(response.status_code, 200)
