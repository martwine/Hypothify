from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from voting.models import Vote



class UTI(models.Model):
	originator=models.ForeignKey(User, editable=False)
	created_date=models.DateTimeField(auto_now_add=True, editable=False)
	
	class Meta:
		abstract = True
		
	def get_absolute_url(self):
		return "/item/%i" % self.id

	def get_votes(self):
		ctype = ContentType.objects.get_for_model(self)
		return Vote.objects.get(content_type=ctype, object_id=self.id) 
	
	def get_votescore(self):
		numbers=Vote.objects.get_score(self)
		return numbers['score']
		
	def __unicode__(self):
		return self.content
	


class Description(UTI):
	content=models.CharField("description of hypothesis / evidence item",max_length=200)
	desc_type=models.ForeignKey(ContentType)
	object_id=models.PositiveIntegerField()
	desc_object=generic.GenericForeignKey('desc_type','object_id')
	class Meta(UTI.Meta):
		db_table='description'


class Summary(UTI):
	content = models.TextField("summary of hypothesis / evidence item")
	summ_type=models.ForeignKey(ContentType)
	object_id=models.PositiveIntegerField()
	summ_object=generic.GenericForeignKey('summ_type','object_id')
	class Meta(UTI.Meta):
		db_table='summary'


class Commentary(UTI):
	content=models.TextField("commentary on hypothesis")
	hypothesis=models.ForeignKey('hypotheses.Hypothesis') 
	class Meta(UTI.Meta):
		db_table='hypothesis_commentary'

