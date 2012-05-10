from hypotheses.views import detail
from django.conf.urls.defaults import *
from django.views.generic import ListView,CreateView
from django.contrib.auth.decorators import login_required
from hypotheses.models import Hypothesis

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     #home view
     url(r'^$', ListView.as_view(model=Hypothesis,)),

     #accounts (login, logout etc)
     (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
     (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
     url(r'^hypothesis/(?P<hypothesis_id>\d+)/$','hypotheses.views.detail'),
     url(r'^hypothesis/add', login_required(CreateView.as_view(model=Hypothesis))),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
      url(r'^admin/', include(admin.site.urls)),
)
