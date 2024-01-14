## Instructions for Installing Dependencies:

```bash
# Install pipenv (if not already installed)
pip install pipenv

# Create a virtual environment and install dependencies
pipenv install --dev

# Activate the virtual environment
pipenv shell
```

## Install Dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

## Modify Settings Files:

Turn Debug On
```bash
DEBUG = True
```

Change allowed hosts
```bash
ALLOWED_HOSTS = ["*"]
```

Comment the following part in the settings
```bash
# if 'REDIS_URL' in os.environ:
#     CACHES = {
#         "default": {
#             "BACKEND": "django_redis.cache.RedisCache",
#             "LOCATION": os.environ.get('REDIS_URL'),
#             "OPTIONS": {
#                 "CLIENT_CLASS": "django_redis.client.DefaultClient",
#                 "ssl_cert_reqs": None
#             }
#         }
#     }

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# PORT = int(os.environ.get('PORT', 5000))
```

Change Channel layers to
```bash
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

## Run Redis on Docker
```bash
docker run --rm -p 6379:6379 redis:7
```

## Finally, Run Backend
```bash
python manage.py runserver
```
