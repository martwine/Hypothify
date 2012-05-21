# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView
from UTIs.forms import DescriptionForm, SummaryForm
from UTIs.models import Summary
from hypotheses.models import Hypothesis
from evidences.models import Evidence



class DescriptionCreate(CreateView):
    form_class=DescriptionForm

    def form_valid(self,form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.originator = self.request.user
        self.object.desc_object = Hypothesis.objects.get(id=self.kwargs['hypothesis_id']) if 'hypothesis_id' in self.kwargs else Evidence.objects.get(id=self.kwargs['evidence_id'])
        self.object.save()
        redirect_url = '/hypothesis/%s' % self.kwargs['hypothesis_id'] if 'hypothesis_id' in self.kwargs else '/evidence/%s' % self.kwargs['evidence_id']
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
        self.object.summ_object = Hypothesis.objects.get(id=self.kwargs['hypothesis_id']) if 'hypothesis_id' in self.kwargs else Evidence.objects.get(id=self.kwargs['evidence_id'])
        
        self.object.save()
        redirect_url = '/hypothesis/%s' % self.kwargs['hypothesis_id'] if 'hypothesis_id' in self.kwargs else '/evidence/%s' % self.kwargs['evidence_id']
        return HttpResponseRedirect(redirect_url)
    
class HypothesisSummaryList(ListView):
        
        context_object_name = "summary_list"
        def get_queryset(self):
            hypothesis = get_object_or_404(Hypothesis, id__exact=self.kwargs['hypothesis_id'])
            idlist=[x.id for x in hypothesis.get_ordered_summary_items()]
            return Summary.objects.filter(id__in=idlist)
        
        def get_context_data(self, **kwargs):
            # Call the base implementation first to get a context
            context = super(HypothesisSummaryList, self).get_context_data(**kwargs)
            # Add in a QuerySet of all the books
            hypothesis = get_object_or_404(Hypothesis, id__exact=self.kwargs['hypothesis_id'])
            context['h'] = hypothesis
            return context  