from django.conf import settings

def hypothify_global(request):
    return {
            'urlbase':settings.URLBASE
    }
