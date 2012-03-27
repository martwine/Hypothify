from django.shortcuts import render_to_response, get_object_or_404
from hypotheses.models import Hypothesis
from evidences.models import Evidence

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
