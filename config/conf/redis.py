CACHES = {
    "default": {
        "BACKEND": 'django_redis.cache.RedisCache',
        "LOCATION": 'redis://127.0.0.1:6379/1',
        "TIMEOUT": 5,
    },
}

CACHE_MIDDLEWARE_SECONDS = 5


CACHEOPS_REDIS = 'redis://127.0.0.1:6379/1'
CACHEOPS_DEFAULTS = {
    "timeout": 5,
}

CACHEOPS = {
    "accounts.*": {
        "ops": "all", 
        "timeout": 60 * 5,
    },
    "company.*": {
        "ops": "all",
        "timeout": 60 * 5
    },
    "products.*": {
        "ops": "all",
        "timeout": 60 * 5
    },
    "projects.*": {
        "ops": "all",
        "timeout": 60 * 5
    },
    "wherehouse.*": {
        "ops": "all",
        "timeout": 60 * 5
    },
    "shared.*": {
        "ops": "all",
        "timeout": 60 * 5
    },
    
}
CACHEOPS_DEGRADE_ON_FAILURE = True
CACHEOPS_ENABLED = False