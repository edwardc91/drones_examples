from django.contrib.auth.models import User

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from base.models import Drone, Medication

import logging
logger = logging.getLogger(__name__)

class DroneViewSetTests(APITestCase):
    base_url = 'http://127.0.0.1:8000'

    def add_test_drone(self):
        """
        Adds a test drone into the database
        """

        logger.debug('Adding a new drone into database')
        p = Drone(serial_number='testdrone01')
        p.save()
        logger.debug('Successfully added test drone into the database')
        return p

    def add_user_and_setup_token(self):
        user = User.objects.create_user(username='admin', email='admin@admin.com', password='admin')
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def add_test_medication(self):
        """
        Adds a test medication into the database
        """

        logger.debug('Adding a new medication into database')
        m = Medication(name='testmedication01', code='LLLL-HHHHH', weight=10)
        m.save()
        logger.debug('Successfully added test medication into the database')
        return m

    def test_list_drones(self):
        """
        Test to list all the drones in the list
        """

        logger.debug('Starting test list drones')

        self.add_test_drone()
        self.add_user_and_setup_token()

        url = self.base_url + reverse('drones-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url, format='json')
        json = response.json()

        logger.debug('Testing status code response: %s, code: %d'%(json, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug('Testing result count')
        self.assertEqual(json['meta']['total_results'], 1)

    def test_create_drone(self):
        """
        Tests creating a new drone object
        """

        self.add_user_and_setup_token()

        logger.debug('Starting test create drone')
        url = self.base_url + reverse('drones-list')

        data = {
            'serial_number' : 'HHHH-989-LLLL',
        }

        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.post(url, data, format='json')
   
        logger.debug('Testing status code response: %s, code: %d'%(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        logger.debug('Testing drone count to make sure object was successfully added')
        self.assertEqual(Drone.objects.count(), 1)

        logger.debug('Testing new drone object details')
        d = Drone.objects.get()
        self.assertEqual(d.serial_number, 'HHHH-989-LLLL')
        self.assertEqual(d.weight_limit, 500)
        self.assertEqual(d.state, 'IDLE')

        logger.debug('Test drone create completed successfully')

    def test_create_drone_invalid_weight(self):
        """
        Tests creating a new drone object with invalid weight
        """
        
        self.add_user_and_setup_token()

        logger.debug('Starting test create drone')
        url = self.base_url + reverse('drones-list')

        data = {
            'serial_number' : 'HHHH-989-LLLL',
            'weight_limit' : 501,
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

    def test_create_drone_invalid_battery(self):
        """
        Tests creating a new drone object with invalid battery
        """
        
        self.add_user_and_setup_token()

        logger.debug('Starting test create drone')
        url = self.base_url + reverse('drones-list')

        data = {
            'serial_number' : 'HHHH-989-LLLL',
            'battery_capacity' : 101,
        }

        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.post(url, data, format='json')
   
        logger.debug('Testing status code response: %s, code: %d'%(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data['battery_capacity'] = -1
        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.post(url, data, format='json')
   
        logger.debug('Testing status code response: %s, code: %d'%(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_load_to_drone(self):
        """
        Test adding a load to a drone
        """

        self.add_user_and_setup_token()
        drone = self.add_test_drone()
        medication = self.add_test_medication()

        logger.debug('Starting test create drone')
        url = self.base_url + '/drones/{}/load_addition/'.format(drone.id)

        data = {
            'quantity' : 2,
            'medication' : medication.id,
        }

        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.patch(url, data, format='json')
   
        logger.debug('Testing status code response: %s, code: %d'%(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url_load_weight = self.base_url + '/drones/{}/current_load_weight/'.format(drone.id)

        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.get(url_load_weight, format='json')

        json = response.json()

        logger.debug('Testing status code response: %s, code: %d'%(json, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json["current_load"], 20)

        data = {
            'quantity' : 2,
            'medication' : medication.id,
        }

        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.patch(url, data, format='json')
   
        logger.debug('Testing status code response: %s, code: %d'%(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.get(url_load_weight, format='json')

        json = response.json()

        logger.debug('Testing status code response: %s, code: %d'%(json, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json["current_load"], 40)


