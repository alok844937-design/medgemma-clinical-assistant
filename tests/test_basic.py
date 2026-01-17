import unittest
import sys
sys.path.insert(0, '..')
from app import app, MedGemmaModel

class TestMedGemmaApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.model = MedGemmaModel()
    
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_health_endpoint(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
    
    def test_patient_mode_processing(self):
        test_text = "Patient has hypertension and myocardial infarction"
        result = self.model.process_patient_explanation(test_text)
        self.assertIn('high blood pressure', result.lower())
        self.assertIn('heart attack', result.lower())
    
    def test_doctor_mode_processing(self):
        test_text = "Patient presents with chest pain"
        result = self.model.process_doctor_structure(test_text)
        self.assertIn('Clinical Summary', result)
    
    def test_api_patient_endpoint(self):
        response = self.app.post('/api/process',
            json={'text': 'hypertension', 'mode': 'patient'}
        )
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()