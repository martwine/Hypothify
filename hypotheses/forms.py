from django.forms import ModelForm
from hypotheses.models import Hypothesis

#exclude status field from generic view
class HypothesisForm(ModelForm):
    class Meta:
        model = Hypothesis
        exclude=('status','proposer')