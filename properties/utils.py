from django.core.cache import cache
from django_redis import get_redis_connection
import redis
import logging


from .models import Property


logger = logging.getLogger(__name__)

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

def get_redis_cache_metrics():
    try:
        # Get a raw redis-py client
        redis_client = get_redis_connection("default")

        info = redis_client.info()  # same as redis-cli INFO

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        total_requests = hits + misses
        hit_ratio = (hits / total_requests) if total_requests > 0 else 0

        return {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 3),
        }
    except redis.ConnectionError as e:
        logger.error("Redis connection failed: %s", e, exc_info=True)
        return None
    except redis.TimeoutError as e:
        logger.error("Redis operation timed out: %s", e, exc_info=True)
        return None
    except Exception as e:
        # Catch-all for other Redis or Django cache errors
        logger.error("Unexpected Redis error: %s", e, exc_info=True)
        return None