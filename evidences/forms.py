from django.forms import ModelForm
from django.contrib.contenttypes.generic import generic_inlineformset_factory

from evidences.models import Evidence
from UTIs.models import Description


#exclude status field from generic view
class EvidenceForm(ModelForm):
    class Meta:
        model = Evidence
        exclude=('introducer','hypothesis')

#DescriptionEvidenceFormSet = inlineformset_factory(Evidence, DescriptionForm,fk_name="descriptions")    
EvidenceDescriptionFormSet = generic_inlineformset_factory(Description, EvidenceForm, ct_field='desc_type', extra=1)


