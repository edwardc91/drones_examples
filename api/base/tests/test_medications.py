from django.contrib.auth.models import User

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from base.models import Medication

import logging
logger = logging.getLogger(__name__)

class MedicationViewSetTests(APITestCase):
    base_url = 'http://127.0.0.1:8000'

    def add_test_medication(self):
        """
        Adds a test medication into the database
        """

        logger.debug('Adding a new medication into database')
        m = Medication(name='testmedication01', code='LLLL-HHHHH')
        m.save()
        logger.debug('Successfully added test medication into the database')

    def add_user_and_setup_token(self):
        user = User.objects.create_user(username='admin', email='admin@admin.com', password='admin')
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_list_medications(self):
        """
        Test to list all the medications in the list
        """

        logger.debug('Starting test list medications')

        self.add_test_medication()
        self.add_user_and_setup_token()

        url = self.base_url + reverse('medications-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url, format='json')
        json = response.json()

        logger.debug('Testing status code response: %s, code: %d'%(json, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug('Testing result count')
        self.assertEqual(json['meta']['total_results'], 1)

    def test_create_medication(self):
        """
        Tests creating a new medication object
        """

        self.add_user_and_setup_token()

        logger.debug('Starting test create medication')
        url = self.base_url + reverse('medications-list')

        data = {
            'code' : 'HHHH-989-LLLL',
            'name': 'Test medication',
            'weight': 10
        }

        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.post(url, data, format='json')
   
        logger.debug('Testing status code response: %s, code: %d'%(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        logger.debug('Testing medication count to make sure object was successfully added')
        self.assertEqual(Medication.objects.count(), 1)

        logger.debug('Testing new medication object details')
        d = Medication.objects.get()
        self.assertEqual(d.code, 'HHHH-989-LLLL')
        self.assertEqual(d.weight, 10)
        self.assertEqual(d.name, 'Test medication')

        logger.debug('Test medication create completed successfully')

    def test_create_medication_invalid_weight(self):
        """
        Tests creating a new medication object with invalid weight
        """
        
        self.add_user_and_setup_token()

        logger.debug('Starting test create medication')
        url = self.base_url + reverse('medications-list')

        data = {
            'code' : 'HHHH-989-LLLL',
            'name': 'Test medication',
            'weight' : 501,
        }

        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.post(url, data, format='json')
   
        logger.debug('Testing status code response: %s, code: %d'%(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data['weight_limit'] = 0
        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.post(url, data, format='json')
   
        logger.debug('Testing status code response: %s, code: %d'%(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_medication_invalid_code(self):
        """
        Tests creating a new medication object with invalid battery
        """
        
        self.add_user_and_setup_token()

        logger.debug('Starting test create medication')
        url = self.base_url + reverse('medications-list')

        data = {
            'code' : 'HHHH-989-lllll',
            'name': 'Test medication',
        }

        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.post(url, data, format='json')
   
        logger.debug('Testing status code response: %s, code: %d'%(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
