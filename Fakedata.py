from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from voting.models import Vote
from voting.managers import VoteManager
from hypotheses.models import Hypothesis
from evidences.models import EvidenceType, Evidence
from UTIs.models import Summary, Description, Commentary


u=User.objects.all()[0]
u2=User.objects.all()[1]
u3=User.objects.all()[2]

h=Hypothesis(proposer=u,originator_name="Joe Bloggs",originator_unique="@joebloggs",status="Straw 			Man",proposer_description="This is a straw man hypothesis")
h.save()
d1=Description(content="This is a straw man hypotheses consisting of basically nothing at 				all",desc_object=h,originator=u)
d1.save()

s1=Summary(content="A boring hypothesis consisteing of nothing much at all blah blah balhhk ahdlhd kjah 		dkahd kadh akjdha kjdh akhd jahdjah duysgf kadsf iuhf oihg kadgf ihf iqgf oieg[oegooigwu iuh weug 			uehf poeuf ieh fieh fue fi [epouoiger w[oejg [owejg oewug", originator=u,summ_object=h)
s1.save()

evt=EvidenceType(name="Journal article")
evt.save()
evt2=EvidenceType(name="blog post")
evt.save()

ev=Evidence(hypothesis=h,url="http://strawman.com", originator_name="Blog Joes",originator_unique="@BJ",introducer=u,uri="strawman",evidence_type=evt)
ev.save()
ed1=Description(content="some evidence shows Xand Y but not Z", originator=u,summ_object=ev)
ed1.save()


ev2=Evidence(hypothesis=h,url="http://stoneman.com", originator_name="Blog Joes",originator_unique="@BJ",introducer=u,uri="stoneman",for_hypothesis=False,evidence_type=evt)
ev2.save()

ev3=Evidence(hypothesis=h,url="httpE	://hayman.com", originator_name="Blog Joes",originator_unique="@BJ",introducer=u,uri="hayman",for_hypothesis=True,evidence_type=evt)
ev3.save()

ev4=Evidence(hypothesis=h,url="http://crap.com", originator_name="Harry Hill", originator_unique="badgerbadger", introducer=u,uri="bollokcs",for_hypothesis=False,evidence_type=evt)
ev4.save()

Vote.objects.record_vote(ev,u,+1)
Vote.objects.record_vote(ev,u3,+1)
Vote.objects.record_vote(ev,u2,+1)
	
	
Vote.objects.record_vote(ev3,u,-1)
Vote.objects.record_vote(ev3,u2,-1)
		
Vote.objects.record_vote(ev2,u,+1)
Vote.objects.record_vote(ev2,u2,+1)
Vote.objects.record_vote(ev2,u3,+1)





