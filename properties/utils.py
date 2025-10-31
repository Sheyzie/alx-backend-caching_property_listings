from django.core.cache import cache

from .models import Property


def get_all_properties():
    # Check cache first
    data = cache.get('all_properties')

    if data is not None:
        return data

    # Otherwise, fetch from DB
    queryset = Property.objects.all()

    # Store in cache for 10 minutes (600 seconds)
    cache.set('all_properties', queryset, 3600)

    return queryset