# Settings specific to production environment
TEMPLATE_DIRS = ('/app/polymath/templates')

STATIC_URL = 'http://s3.amazonaws.com/polymath_static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
