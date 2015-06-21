from django.conf.urls import include, patterns, url
from django.contrib import admin
from paged import views

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^receive/$', views.receive, name='receive')
)