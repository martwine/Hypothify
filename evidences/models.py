from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from hypothify.hypotheses.models import Hypothesis
from hypothify.UTIs.models import Description, Summary

from voting.managers import VoteManager

class EvidenceType(models.Model):
	name=models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.name

class Evidence(models.Model):
	url=models.URLField()
	hypothesis=models.ForeignKey(Hypothesis, related_name='evidenceset')
	originator_name=models.CharField(max_length=100)
	originator_unique=models.CharField(max_length=100)
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

	def get_summaries_voteinfo(self):
		scores=get_scores_in_bulk(self.summaries)
		return scores

	def get_descriptions_voteinfo(self):
		scores=get_scores_in_bulk(self.descriptions)
		return scores
		


		

