from django import forms
from hypotheses.models import Hypothesis

#exclude status field from generic view
class HypothesisForm(forms.ModelForm):
    class Meta:
        model=Hypothesis
        exclude=('status')