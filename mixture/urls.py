from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mixture.views.home', name='home'),
    # url(r'^mixture/', include('mixture.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^image/', 'image.views.index'),
)
