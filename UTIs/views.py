# Create your views here.
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from UTIs.forms import DescriptionForm, SummaryForm
from hypotheses.models import Hypothesis
from evidences.models import Evidence


class DescriptionCreate(CreateView):
    form_class=DescriptionForm

    def form_valid(self,form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.originator = self.request.user
        self.object.desc_object = Hypothesis.objects.get(id=self.kwargs['hypothesis_id']) if self.kwargs['hypothesis_id'] else Evidence.objects.get(id=self.kwargs['evidence_id'])
        self.object.save()
        redirect_url = '/hypothesis/%s' % self.kwargs['hypothesis_id'] if self.kwargs['hypothesis_id'] else '/evidence/%s' % self.kwargs['evidence_id']
        return HttpResponseRedirect(redirect_url)

class SummaryCreate(CreateView):
    form_class=SummaryForm    
    extra_context = {}
    
    def get_context_data(self, **kwargs):
        context = super(SummaryCreate, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context
    
    def form_valid(self,form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.originator = self.request.user
        self.object.summ_object = Hypothesis.objects.get(id=self.kwargs['hypothesis_id']) if self.kwargs['hypothesis_id'] else Evidence.objects.get(id=self.kwargs['evidence_id'])
        
        self.object.save()
        redirect_url = '/hypothesis/%s' % self.kwargs['hypothesis_id'] if self.kwargs['hypothesis_id'] else '/evidence/%s' % self.kwargs['evidence_id']
        return HttpResponseRedirect(redirect_url)