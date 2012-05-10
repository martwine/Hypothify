from django.forms import ModelForm
from hypotheses.models import Hypothesis
from evidences.models import Evidence

#exclude status field from generic view
class EvidenceForm(ModelForm):
    class Meta:
        model = Evidence
        exclude=('introducer','hypothesis')