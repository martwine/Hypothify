from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from evidences.models import Evidence
from UTIs.models import Description, Summary
from voting.models import Vote
from django.conf import settings




class Hypothesis(models.Model):
	proposer=models.ForeignKey(User,related_name='hypothesis_proposerset',editable=False)
	proposer_description=models.CharField(max_length=200, help_text="describe the hypothesis in 200 characters or less", verbose_name="Hypothesis")
	originator_name=models.CharField(max_length=100, help_text="Name of person who originally proposed hypothesis. If it is your hypothesis, type \'me\'")
	originator_unique=models.CharField(max_length=100, blank=True, editable=False)
	originator_user=models.ForeignKey(User, blank=True, null=True, related_name='hypothesis_originatorset', editable=False)
	status=models.CharField(max_length=50, blank=True, null=True, editable=False)
		
	#map back generic relations to Summaries and Descriptions
	summaries = generic.GenericRelation(Summary, content_type_field='summ_type',object_id_field='object_id')
	descriptions = generic.GenericRelation(Description, content_type_field='desc_type',object_id_field='object_id')
	
	def __unicode__(self):
		return self.proposer_description
	
	def get_absolute_url(self):
		return "%shypothesis/%s/" % (settings.URLBASE, self.id)

	def get_disqus_id(self):
		return "hypothesis_%s" % self.id

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
		#in_bulk doesn't preserve order to need to reorder afterwards
		unordered = Evidence.objects.in_bulk(all_ids)	
		reordered = [unordered.get(id,None) for id in all_ids]
		return filter(None, reordered)

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
