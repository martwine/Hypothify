from django import forms
from django.contrib.contenttypes.generic import generic_inlineformset_factory as inlineformset_factory
from hypotheses.models import Hypothesis
from UTIs.models import Summary

#exclude status field from generic view
class HypothesisForm(forms.ModelForm):
    
    class Meta:
        model = Hypothesis
        widgets={'proposer_description':forms.Textarea(attrs={'cols':50,'rows':4,'max_length':200}),}

HypothesisSummaryFormSet = inlineformset_factory(Summary, HypothesisForm, ct_field='summ_type', extra=1)