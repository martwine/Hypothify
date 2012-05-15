from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from UTIs.models import Description, Summary
from voting.models import Vote

class EvidenceType(models.Model):
	name=models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.name

class Evidence(models.Model):
	url=models.URLField()
	hypothesis=models.ForeignKey('hypotheses.Hypothesis', related_name='evidenceset')
	originator_name=models.CharField(max_length=100)
	originator_unique=models.CharField(max_length=100, blank=True)
	originator_user=models.ForeignKey(User, blank=True, null=True)
	introducer=models.ForeignKey(User, related_name='evidence_introducerset')
	for_hypothesis=models.BooleanField(default=True)
	uri=models.SlugField(max_length=100)
	evidence_type=models.ForeignKey(EvidenceType, related_name='evidenceset_of_this_type')

	#map back generic relations to Summary and Descriptions
	summaries = generic.GenericRelation(Summary, content_type_field='summ_type',object_id_field='object_id')
	descriptions = generic.GenericRelation(Description, content_type_field='desc_type',object_id_field='object_id')

	def __unicode__(self):
		return self.url
	
	def get_absolute_url(self):
		return settings.URLBASE  + "/evidence" + self.id

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
		return [j for i,j in Summary.objects.in_bulk(all_ids).items()]	
	
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
		return [j for i,j in Description.objects.in_bulk(all_ids).items()]

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


		

