from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mixture.views.home', name='home'),
    # url(r'^mixture/', include('mixture.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'views.index'),
    url(r'^process/(....+)', 'views.process'),
    url(r'^poll/(....+)', 'views.poll'),
    url(r'^play/(?P<mxmid>[\w.\+_:-]+)+', 'views.play'),
    url(r'^upload/', 'views.upload'),
    url(r'^tracks/(?P<terms>[\w.\+_:-]+)+', 'views.tracks'),
)
