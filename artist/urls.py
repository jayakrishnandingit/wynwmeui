from django.conf.urls import patterns, include, url

from django.contrib import admin
from .views import HomePage, ArtistList
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wynwmeui.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', HomePage.as_view(), name='home_page'),
    url(r'api/artists$', ArtistList.as_view(), name='artist_list')
)
