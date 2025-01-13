from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .utils import load_model_and_vectorizer, extract_features_from_cv

class CVAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.model, self.vectorizer = load_model_and_vectorizer()

    def test_home_page(self):
        response = self.client.get(reverse('cvapp:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to CV Scanner")

    def test_upload_cv_page(self):
        response = self.client.get(reverse('cvapp:upload_cv'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload CV")

    def test_upload_cv_functionality(self):
        with open('cvapp/test_files/31064969.pdf', 'rb') as cv_file:
            response = self.client.post(reverse('cvapp:upload_cv'), {'cv': cv_file})
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard
        self.assertRedirects(response, reverse('cvapp:dashboard'))

    def test_evaluate_cv_page(self):
        response = self.client.get(reverse('cvapp:evaluate_cv'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Evaluate CV")

    def test_evaluate_cv_functionality(self):
        response = self.client.post(reverse('cvapp:evaluate_cv'), {'features': 'manager, communication, degree'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('prediction', response.json())

    def test_dashboard_page(self):
        session = self.client.session
        session['cv_evaluation'] = 'Suitable'
        session.save()
        response = self.client.get(reverse('cvapp:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CV Evaluation Result")

    def test_feature_extraction(self):
        features = extract_features_from_cv('cvapp/test_files/31064969.pdf')
        self.assertIsNotNone(features)
        self.assertEqual(features.shape[1], len(self.vectorizer.get_feature_names_out()))
# Create your tests here.
