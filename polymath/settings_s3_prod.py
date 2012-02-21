from settings import *

# overrides the S3 bucket name so that collectstatic sends our static files to the production bucket instead of staging (the default) 
AWS_STORAGE_BUCKET_NAME = 'polymath_static'
