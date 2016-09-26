from django.test import TestCase
from weather.api import WeatherAPI
from django.conf import settings

class WeatherAPICase(TestCase):

	KNOWN_CITY = 'London, GB'
	UNKNOWN_CITY = 'dasdas#2132'
	KEYS = ['max_temp','min_temp','period','avg_temp','avg_hum']

	def setUp(self):
		WeatherAPI(settings.API_URL,settings.API_KEY)

	def test_load_know_city(self):
		api = WeatherAPI(settings.API_URL,settings.API_KEY)
		self.assertTrue(all(k in api.get_forecast(self.KNOWN_CITY) for k in self.KEYS))

	def test_load_unknow_city(self):
		api = WeatherAPI(settings.API_URL,settings.API_KEY)
		self.assertEqual(api.get_forecast(self.UNKNOWN_CITY)['message'],"Error: Not found city")
