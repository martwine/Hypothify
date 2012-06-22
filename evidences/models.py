from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.conf import settings
from UTIs.models import Description, Summary
from voting.models import Vote

class EvidenceType(models.Model):
	name=models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.name

class Evidence(models.Model):
	url=models.URLField(help_text="http address of evidence item e.g. http://nature.com/articles/291_223/")
	hypothesis=models.ForeignKey('hypotheses.Hypothesis', related_name='evidenceset', editable=False)
	originator_name=models.CharField(max_length=100,verbose_name="originator citation",help_text="The name of the author of the evidence or better still a dated citation for the evidence e.g. \'Gable et al 2003\' or \'Clark Gable\'")
	originator_unique=models.CharField(max_length=100, blank=True, editable=False)
	originator_user=models.ForeignKey(User, blank=True, null=True, editable=False)
	introducer=models.ForeignKey(User, related_name='evidence_introducerset', editable=False)
	for_hypothesis=models.BooleanField(default=True,verbose_name="Is this evidence in support of the hypothesis?",help_text="de-select if evidence is against the hypothesis")
	doi=models.CharField(max_length=100,blank=True,help_text="add doi without prefixes i.e. 10.1029/30212JJ3 not doi:10.1029/30212JJ3")
	evidence_type=models.ForeignKey(EvidenceType, related_name='evidenceset_of_this_type',verbose_name="Evidence type",help_text="If you can't find the right type, select \'other\' and let us know")

	#map back generic relations to Summary and Descriptions
	summaries = generic.GenericRelation(Summary, content_type_field='summ_type',object_id_field='object_id')
	descriptions = generic.GenericRelation(Description, content_type_field='desc_type',object_id_field='object_id')

	def __unicode__(self):
		return self.url
	
	def get_absolute_url(self):
		return "%sevidence/%s/" %(settings.URLBASE,self.id)

	def For(self):
		if self.for_hypothesis:
			return "For"
		else:
			return "Against"
	
	def lcfor(self):
		if self.for_hypothesis:
			return "for"
		else:
			return "against"
	
	def get_summaries_voteinfo(self):
		scores=Vote.objects.get_scores_in_bulk(self.summaries.all())
		return scores

	def get_top_summary_ids(self):
		scores=self.get_summaries_voteinfo()
		sorted_ids=sorted(scores, key=lambda x: (scores[x]['score'],scores[x]['num_up_votes']),reverse=True)
		return sorted_ids

	def get_ordered_summary_items(self):
		voted_ids=self.get_top_summary_ids()
		other_ids=[item.id for item in self.summaries.exclude(id__in=voted_ids)]
		all_ids=voted_ids+other_ids
		unordered = Summary.objects.in_bulk(all_ids)	
		reordered = [unordered.get(id,None) for id in all_ids]
		return filter(None, reordered)
	
	def get_top_summary(self):
		return self.get_ordered_summary_items()[0]
		
	def get_descriptions_voteinfo(self):
		scores=Vote.objects.get_scores_in_bulk(self.descriptions.all())
		return scores
		
	def get_top_description_ids(self):
		scores=self.get_descriptions_voteinfo()
		sorted_ids=sorted(scores, key=lambda x: (scores[x]['score'],scores[x]['num_up_votes']),reverse=True)
		return sorted_ids	
	
	def get_ordered_description_items(self):
		voted_ids=self.get_top_description_ids()
		other_ids=[item.id for item in self.descriptions.exclude(id__in=voted_ids)]
		all_ids=voted_ids+other_ids
		unordered = Description.objects.in_bulk(all_ids)	
		reordered = [unordered.get(id,None) for id in all_ids]
		return filter(None, reordered)

	def get_top_description(self):
		q=self.get_ordered_description_items()
		v=self.descriptions.all()
		if len(q)>0:
			d=q[0]
		elif len(v)>0:
			d=self.descriptions.all()[0]
		else:
			d=None
		return d
		

	def get_votescore(self):
		numbers=Vote.objects.get_score(self)
		return numbers['score']


		

