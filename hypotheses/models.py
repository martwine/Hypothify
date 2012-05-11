from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from evidences.models import Evidence
from UTIs.models import Description, Summary
from voting.models import Vote



class Hypothesis(models.Model):
	proposer=models.ForeignKey(User,related_name='hypothesis_proposerset')
	proposer_description=models.CharField(max_length=200)
	originator_name=models.CharField(max_length=100)
	originator_unique=models.CharField(max_length=100, blank=True)
	originator_user=models.ForeignKey(User, blank=True, null=True, related_name='hypothesis_originatorset')
	status=models.CharField(max_length=50, blank=True, null=True)
		
	#map back generic relations to Summaries and Descriptions
	summaries = generic.GenericRelation(Summary, content_type_field='summ_type',object_id_field='object_id')
	descriptions = generic.GenericRelation(Description, content_type_field='desc_type',object_id_field='object_id')
	
	def __unicode__(self):
		return self.proposer_description
	
	def get_absolute_url(self):
		return "/hypothesis/%i" % self.id

	def get_evidences_voteinfo(self):
		scores=Vote.objects.get_scores_in_bulk(self.evidenceset.all())
		return scores

	def get_top_evidence_ids(self):
		#use e.g. Evidence.objects.in_bulk(<hypothesis>.get_top_evidences)
		scores=self.get_evidences_voteinfo()
		sorted_ids=sorted(scores, key=lambda x: (scores[x]['score'],scores[x]['num_up_votes']),reverse=True)
		return sorted_ids

	def get_ordered_evidence_items(self):
		voted_ids=self.get_top_evidence_ids()
		other_ids=[item.id for item in self.evidenceset.exclude(id__in=voted_ids)]
		all_ids=voted_ids+other_ids
		return [j for i,j in Evidence.objects.in_bulk(all_ids).items()]	

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
