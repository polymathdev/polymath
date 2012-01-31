from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import redirect_to, direct_to_template
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^test/', 'core.views.test'),

	# 404 test
    (r'^404test/', direct_to_template, {'template':'404.html'}),

	#500 test
    (r'^500test/', direct_to_template, {'template':'500.html'}),

    # home page
    (r'^$', 'core.views.home_page'),

    # welcome
    (r'^welcome/', 'core.views.welcome'), 

	#about
    (r'^about/', direct_to_template, {'template':'about.dtl'}),

	#beliefs
    (r'^beliefs/', direct_to_template, {'template':'beliefs.dtl'}),

	#howitworks
    (r'^howitworks/', direct_to_template, {'template':'howitworks.dtl'}),

	#contact
    (r'^contact/', direct_to_template, {'template':'contact.dtl'}),
	
    # auth
    url(r'^login/$','django.contrib.auth.views.login', {'template_name':'registration/login.dtl'}, name='login'),
    url(r'^logout/$','django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'', include('social_auth.urls')),

    # auth testing
    (r'^logintest/$', 'django.contrib.auth.views.login', {'template_name':'registration/logintest.dtl'}),

    # view profile
    url(r'^myprofile/$','core.views.view_myprofile', name='view_my_profile'),
    url(r'^profile/(?P<uname>[a-z0-9]+)/$','core.views.view_profile', name='view_profile'), 

    # add / edit courses
    url(r'^courses/add/$','core.views.add_course', name='add_course'),   
    url(r'^courses/(?P<course_id>\d+)/edit/$','core.views.edit_course', name='edit_course'),

    # browse courses
    url(r'^courses/$', redirect_to, {'url' : '/courses/browse' } ),
    url(r'^courses/browse/$', 'core.views.browse_courses', name='browse_courses_all'),
    url(r'^courses/browse/(?P<cat_slug>[a-zA-Z0-9-]+)/$', 'core.views.browse_courses', name='browse_courses_by_cat'),
    url(r'^courses/browse/(?P<cat_slug>[a-zA-Z0-9-]+)/(?P<tag_slug>[a-zA-Z0-9-]+)/$', 'core.views.browse_courses', name='browse_courses_by_cat_and_tag'),

    # view course (can the below 2 URL regexes be combined? probably, but just tried something real quick and it didn't work so will revisit when i have less things that are higher priority)
    url(r'^courses/(?P<course_id>\d+)/(?P<course_slug>[a-zA-Z0-9-]*)/$','core.views.view_course', name='view_course'),
    url(r'^courses/(?P<course_id>\d+)/$','core.views.view_course', name='view_course_noslug'), 

    # misc ajax actions
    url(r'^deletelesson/$','core.views.delete_lesson', name='delete_lesson'),
    url(r'^completelesson/$', 'core.views.complete_lesson', name='complete_lesson'),
    url(r'^votelesson/$', 'core.views.vote_lesson', name='vote_lesson'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

     # comments
    (r'^comments/', include('simple_comments.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
