from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from evidences.forms import EvidenceForm
from hypotheses.models import Hypothesis



class EvidenceCreate(CreateView):
    form_class=EvidenceForm    
    
    def form_valid(self,form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.introducer = self.request.user
        self.object.hypothesis = Hypothesis.objects.get(id=self.kwargs['hypothesis_id'])
        self.object.save()
        redirect_url = '/hypothesis/%s' % self.kwargs['hypothesis_id']
        return HttpResponseRedirect(redirect_url)
