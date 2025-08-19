CACHES = {
    "default": {
        "BACKEND": 'django_redis.cache.RedisCache',
        "LOCATION": 'redis://redis:6379',
        "TIMEOUT": 300,
    },
}

CACHE_MIDDLEWARE_SECONDS = 300


CACHEOPS_REDIS = 'redis://redis:6379'
CACHEOPS_DEFAULTS = {
    "timeout": 300,
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
    "company.Company":{
        "ops": "all",
        "timeout": 300,
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