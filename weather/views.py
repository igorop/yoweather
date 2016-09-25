from random import randint

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404
from django.template import Context
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions

from weather.forms import WeatherForm
from weather.api import WeatherAPI

from serializers import *

# Page View

def app_view(request, template_name='app_page.html'):

	# random background cover
	cover = randint(1,6)

	return render_to_response(template_name, {
		'cover': cover
    }, RequestContext(request))


# Weather API

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def forcast_api(request):
    """
    List all snippets, or create a new snippet.
    """

    serializer = ForecastSerializer(data=request.GET)
    if serializer.is_valid():

    	api = WeatherAPI(
    		settings.API_URL,
    		settings.API_KEY
    	)

    	response_data = api.get_forecast(city=serializer.data['city'],period=serializer.data['period'])

    	return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


