from hypotheses.views import detail
from django.conf.urls.defaults import *
from django.views.generic import ListView
from hypotheses.models import Hypothesis

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', ListView.as_view(model=Hypothesis,)),
     url(r'^hypotheses/(?P<hypothesis_id>\d+)/$','hypotheses.views.detail'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
      url(r'^admin/', include(admin.site.urls)),
)
