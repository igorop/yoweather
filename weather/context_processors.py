from django.conf import settings # import the settings file

def site_info(request):
    return {
        'SITE_URL': settings.SITE_URL,
        'SITE_NAME': settings.SITE_NAME,
        'SITE_SLOGAN': settings.SITE_SLOGAN
    }
