from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Admin
	url(r'^admin/', include(admin.site.urls)),

	# User auth url
	url(r'^$', 'app.views.landing', name ='landing'),
	url(r'^profile/$', 'app.views.profile', name = 'profile'),
	url(r'^product&(\d+)$', 'app.views.product', name='product'),
	#url(r'^auth/$', 'app.views.auth_view', name='user_auth'),
	#url(r'^invalid/$', 'app.views.invalid_login', name='invalid_login'),
	
	# Test form
	url(r'^register$', 'app.views.register', name='register'),
    url(r'^login$', 'app.views.login', name='login'),
    url(r'^logout$', 'app.views.logout', name='logout'),
)

from django.conf import settings
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'%s(?P<path>.*)' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)