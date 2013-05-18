from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'help_student.views.home', name='home'),
    url(r'^register/$', 'help_student.views.register', name='cadastro'),
    url(r'^matter/$', 'help_student.views.register_matter', name='materia'),
    url(r'^accounts/profile/$', 'help_student.views.profile', name='profile'),
    url(r'/status/$', 'help_student.views.status_matter', name='status'),
    url(r'^ranking/$', 'help_student.views.ranking', name='ranking'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),


    # url(r'^Help_Student/', include('Help_Student.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
