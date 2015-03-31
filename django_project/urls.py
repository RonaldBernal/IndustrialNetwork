from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # core url
    url(r'^$', 'app.views.landing', name ='landing'),
    url(r'^profile/', 'app.views.profile', name = 'profile'),
    url(r'^product/(\d+)', 'app.views.product', name='product'),
    url(r'^product/new$', 'app.views.new_product', name='product'),
    
    # User auth url
    url(r'^register/', 'app.views.register', name='register'),
    url(r'^login/', 'app.views.login', name='login'),
    url(r'^logout/', 'app.views.logout', name='logout'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'%s(?P<path>.*)' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )