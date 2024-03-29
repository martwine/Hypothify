from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
	user=models.OneToOneField(User)
	
	score=models.IntegerField(default=0)
	url=models.CharField(max_length=200, blank=True)
	full_name=models.CharField(max_length=100, blank=True)

	def create_user_profile(sender,instance, **kwargs):
		profile, created = UserProfile.objects.get_or_create(user=instance)

	post_save.connect(create_user_profile, sender=User)

	#monkey patch to get shortcut e.g. user.profile.score
	User.profile = property(lambda u: u.get_profile() )
	
	def name(self):
		return self.full_name if self.full_name else self.user.name
