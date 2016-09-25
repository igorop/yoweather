import requests, json, math
from datetime import datetime
from django.conf import settings

class UnknownPeriod(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)

class WeatherAPI:

	PERIODS = {
		"today":"",
		"week":"/daily",
	}

	def __init__(self, url, api_key):
		self.url = url
		self.api_key = api_key

	def __fetch_request(self, url, payload={}):
		""" Does the HTTP request to the weather API """

		payload['appid'] = self.api_key
		return requests.get(url, params=payload)

	def __get_stats(self, data):

		temperatures = map(lambda x:x['temperature'],data)
		humidities = map(lambda x:x['humidity'],data)

		max_temp = max(temperatures)
		min_temp = min(temperatures)

		avg_temp = reduce(
			lambda x, y: x + y,
			temperatures
		) / len(data)

		avg_hum = reduce(
			lambda x, y: x + y,
			humidities
		) / len(data)

		return {
			"avg_temp": avg_temp,
			"min_temp": min_temp,
			"max_temp": max_temp,
			"avg_hum": avg_hum
		}

	def __today_forecast(self, data):

		data['list'] = filter(
			lambda x: datetime.utcfromtimestamp(x['dt']).date() == datetime.today().date(),
			data['list']
		)

		return map(lambda x: {
				'period': datetime.utcfromtimestamp(x['dt']).time().strftime('%H:%M'),
				'temperature':int(math.floor(x['main']['temp'])),
				'humidity':x['main']['humidity'],
				'icon':''.join(['http://openweathermap.org/img/w/',x['weather'][0]['icon'],'.png']),
				'description':x['weather'][0]['description']
			}, data['list']
		)


	def __weekly_forecast(self, data):

		return map(lambda x: {
				'period': datetime.utcfromtimestamp(x['dt']).date().strftime('%A'),
				'temperature':int(math.floor(x['temp']['day'])),
				'humidity':x['humidity'],
				'icon':''.join(['http://openweathermap.org/img/w/',x['weather'][0]['icon'],'.png']),
				'description':x['weather'][0]['description']
			}, data['list']
		)


	def get_forecast(self, city,period="today",mode="json"):
		""" Get a forecast for a city and a time period """

		if period not in self.PERIODS.keys():
			raise UnknownPeriod(period)

		url = ''.join([self.url, self.PERIODS[period]])

		request = self.__fetch_request(url=url, payload={
			'q': city,
			'mode': 'json',
			'units': 'metric'
		})

		data = json.loads(request.text)

		try:

			if period == 'today':
				period = self.__today_forecast(data)
			else:
				period = self.__weekly_forecast(data)

			response_load = self.__get_stats(period)
			response_load['period'] = period
		except:
			response_load = data

		return response_load

