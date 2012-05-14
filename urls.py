from django.conf.urls.defaults import *
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required


from hypotheses.views import detail, HypothesisCreate
from hypotheses.models import Hypothesis
from evidences.models import Evidence
from evidences.views import EvidenceCreate
from UTIs.models import Description, Summary
from UTIs.views import SummaryCreate, DescriptionCreate 


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     #home view
     url(r'^$', ListView.as_view(model=Hypothesis,)),

     #accounts (login, logout etc)
     (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
     (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
     
     url(r'^hypothesis/add', login_required(HypothesisCreate.as_view(model=Hypothesis))),
     url(r'^hypothesis/(?P<hypothesis_id>\d+)/$',detail),
     url(r'^hypothesis/(?P<hypothesis_id>\d+)/add_evidence/$', login_required(EvidenceCreate.as_view(model=Evidence))),
     url(r'^hypothesis/(?P<hypothesis_id>\d+)/add_description/$', login_required(DescriptionCreate.as_view(model=Description))),
     url(r'^hypothesis/(?P<hypothesis_id>\d+)/add_summary/$', login_required(SummaryCreate.as_view(model=Summary))),
     
     
     
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
      url(r'^admin/', include(admin.site.urls)),
)
