from django.conf.urls import patterns, include, url
from django.contrib import admin

# (.+) == regex capture group
# (\d+) == regex captures only digits

urlpatterns = patterns('',
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^lists/', include('lists.urls')),
    #url(r'^admin/', include(admin.site.urls)),
)
