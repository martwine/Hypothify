from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext    
from django.views.generic import CreateView, UpdateView
from evidences.models import Evidence
from evidences.forms import EvidenceForm  
from evidences.forms import EvidenceDescriptionFormSet
from hypotheses.models import Hypothesis
from UTIs.models import Description


class EvidenceCreate(CreateView):
    form_class=EvidenceForm    

    def form_valid(self,form):
        context=self.get_context_data()
        evidencedescription_form=context['evidencedescription_formset']
        if evidencedescription_form.is_valid():
            
            self.object = form.save(commit=False)
            self.object.introducer = self.request.user
            self.object.hypothesis = Hypothesis.objects.get(id=self.kwargs['hypothesis_id'])
            self.object.save()
            redirect_url = self.object.hypothesis.get_absolute_url()
            e=Evidence.objects.get(id=self.object.id)
            evidencedescription_form.instance=e
            instances = evidencedescription_form.save(commit=False)
            for instance in instances:
                d = Description(content=instance.content, originator=self.request.user, desc_object=e)
                d.save()
            return HttpResponseRedirect(redirect_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(EvidenceCreate, self).get_context_data(**kwargs)
        context['permission']=True
        if self.request.POST:
            context['evidencedescription_formset']=EvidenceDescriptionFormSet(self.request.POST, instance=self.object)
        else:
            context['evidencedescription_formset']=EvidenceDescriptionFormSet(instance=self.object)
        return(context)


class EvidenceEdit(UpdateView):
    
    def test_permission(self):
        e=Evidence.objects.get(id=self.kwargs['pk'])
        if self.request.user == e.introducer:
            test = True
        elif self.request.user.is_superuser:
            test = True
        else: test = False
        return test

    def get_context_data(self, **kwargs):
        context = super(EvidenceEdit, self).get_context_data(**kwargs)
        context['permission'] = self.test_permission()
        context['edit'] = True
        return(context)
  

def evidencedetail(request,object_id,**kwargs):

    e=get_object_or_404(Evidence, pk=object_id)

    # get associated items ordered by vote 
    
    d=e.get_ordered_description_items()
    
    #and get the 'best' / first one or return None if there aren't any at all
    d1=d[0] if d else None
    
    h = e.hypothesis
    
    
    return render_to_response(
        'evidences/evidence_detail.html',
            {
                'e':e, 
                'e_dset':d,
                'e_top_desc':d1,
                'h':h
            },
            context_instance=RequestContext(request)
    )