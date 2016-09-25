from rest_framework import serializers

class ForecastSerializer(serializers.Serializer):
    city = serializers.CharField(allow_blank=False)
    period = serializers.ChoiceField(
		choices=(
			('today',"Today's Forcast"),
			('week','Five Day Forcast'),
		),
		allow_blank=False
    )
