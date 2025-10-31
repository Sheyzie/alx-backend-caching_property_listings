from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from .models import Property
from .serializers import PropertySerializer
from .utils import get_all_properties

@api_view(['GET'])
@cache_page(60 * 15)  # cache for 15 minutes
def property_list(request):
    queryset = get_all_properties()
    serializer = PropertySerializer(queryset, many=True)
    data = serializer.data

    return JsonResponse({'data': data})

# @api_view(['GET'])
# def property_list(request):
#      # Check cache first
#     cache_key = "property_list"
#     data = cache.get(cache_key)

#     if data is not None:
#         return Response(data, status=status.HTTP_200_OK)

#     # Otherwise, fetch from DB
#     properties = Property.objects.all()
#     serializer = PropertySerializer(properties, many=True)
#     data = serializer.data

#     # Store in cache for 10 minutes (600 seconds)
#     cache.set(cache_key, data, timeout=600)

#     return Response(data)

