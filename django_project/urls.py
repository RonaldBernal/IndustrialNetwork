from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'app.views.login', name ='login'),
    
    url(r'^profile/', 'app.views.home', name = 'home'),

    url(r'^product/(\d+)$', 'app.views.product', name='product'),
    
    url(r'^admin/', include(admin.site.urls)),

    url(r'^request$', 'app.views.request', name='request'),
)
