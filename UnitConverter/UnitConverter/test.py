#import json
#from django.test import TestCase, Client
#from django.urls import reverse
#
#class ConverterTests(TestCase):
#    def setUp(self):
#        self.client = Client()
#        self.url = reverse('converter')
#
#    def test_get_request(self):
#        response = self.client.get(self.url)
#        self.assertEqual(response.status_code, 200)
#        self.assertTemplateUsed(response, 'template.html')
#
#    def test_post_request_length_conversion(self):
#        data = {
#            'mproperty': 'length',
#            'value': 14,
#            'input_unit': 'centimeter',
#            'output_unit': 'inche'
#        }
#        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
#        self.assertEqual(response.status_code, 200)
#        self.assertEqual(response.json()['result'], 3.94)  # 10 cm to inches
#
#        # Test length conversion from inches to centimeters
#        data['input_unit'] = 'inche'
#        data['output_unit'] = 'centimeter'
#        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
#        self.assertEqual(response.status_code, 200)
#        self.assertEqual(response.json()['result'], 25.4)  # 10 inches to cm
