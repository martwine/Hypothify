from django.shortcuts import render_to_response, get_object_or_404
from hypotheses.models import Hypothesis
from evidences.models import Evidence

def detail(request,hypothesis_id,**kwargs):

	h=get_object_or_404(Hypothesis, pk=hypothesis_id)
	#get list of all evidence items by vote
	e=h.get_top_evidence_items()
	d=h.get_top_description_items()
	s=h.get_top_summary_items()
	#and get the 'best'one, or get the first one if there haven't been any votes yet, or return None if there aren't any at all
	e1=e[0] if e else h.evidenceset.all()[0] if h.evidenceset.all() else None
	d1=d[0] if d else h.descriptions.all()[0] if h.descriptions.all() else None
	s1=s[0] if s else h.summaries.all()[0] if h.summaries.all() else None
	
	return render_to_response(
		'hypothesis_detail.html',
			{
				'h':h,
				'h_eset':e, 
				'h_dset':d, 
				'h_sset':s,
				'h_top_desc':d1,				
				'h_top_summ':s1
			}
	)
