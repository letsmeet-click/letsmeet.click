

def environment(request):
    from django.conf import settings
    return {
        'environment': getattr(settings, 'ENVIRONMENT', None)
    }
