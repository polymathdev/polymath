from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    # simple_comments
    url(r'^post/$', 'simple_comments.views.post', name='simple_comments_post'),
    url(r'^delete/$', 'simple_comments.views.delete', name='simple_comments_delete'),

    # django comments
    (r'', include('django.contrib.comments.urls')),
)
