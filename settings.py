import os

from pagespeed_django.settings import BASE_DIR

ALLOWED_HOSTS = ['intpurple_be.onrender.com']

# Static files (for serving assets correctly)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Use WhiteNoise for static file serving
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    ...
]

# Add this at the end
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
