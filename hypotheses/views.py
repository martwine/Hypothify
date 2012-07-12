from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView
from django.template import RequestContext	
from hypotheses.models import Hypothesis
from hypotheses.forms import HypothesisForm, HypothesisSummaryFormSet
from UTIs.models import Summary


# use special form for Hypothesis create generic view to omit fields and redirect to created object
class HypothesisCreate(CreateView):
	form_class=HypothesisForm
	
	
	def form_valid(self,form):
		context=self.get_context_data()
		hypothesissummary_form=context['hypothesissummary_formset']
		if hypothesissummary_form.is_valid():
			
			self.object = form.save(commit=False)
			self.object.proposer = self.request.user
			self.object.save()
			h=Hypothesis.objects.get(id=self.object.id)
			hypothesissummary_form.instance=h
			instances = hypothesissummary_form.save(commit=False)
			for instance in instances:
				s = Summary(content=instance.content, originator=self.request.user, summ_object=h)
				s.save()
			return HttpResponseRedirect(self.object.get_absolute_url())
		else:
			return self.render_to_response(self.get_context_data(form=form))
	
	def form_invalid(self, form):
		return self.render_to_response(self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(HypothesisCreate, self).get_context_data(**kwargs)
		if self.request.POST:
			context['hypothesissummary_formset']=HypothesisSummaryFormSet(self.request.POST, instance=self.object)
		else:
			context['hypothesissummary_formset']=HypothesisSummaryFormSet(instance=self.object)
		return(context)


class HypothesisEdit(UpdateView):
	def test_permission(self):
		h=Hypothesis.objects.get(id=self.kwargs['pk'])
		if self.request.user == h.proposer:
			test = True
		elif self.request.user.is_superuser:
			test = True
		else: test = False
		return test

	def get_context_data(self, **kwargs):
		context = super(HypothesisEdit, self).get_context_data(**kwargs)
		context['permission'] = self.test_permission()
		context['edit'] = True
		return(context)


def detail(request,hypothesis_id,**kwargs):

	h=get_object_or_404(Hypothesis, pk=hypothesis_id)

	# get associated items ordered by vote 
	e=h.get_ordered_evidence_items()
	d=h.get_ordered_description_items()
	s=h.get_ordered_summary_items()
	
	#and get the 'best' / first one or return None if there aren't any at all
	e1=e[0] if e else None
	d1=d[0] if d else None
	s1=s[0] if s else None
	
	
	
	
	return render_to_response(
		'hypotheses/hypothesis_detail.html',
			{
				'h':h,
				'h_eset':e, 
				'h_dset':d, 
				'h_sset':s,
				'h_top_desc':d1,				
				'h_top_summ':s1
			},
			context_instance=RequestContext(request)
	)


