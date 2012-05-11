from django.forms import ModelForm
from UTIs.models import Description, Summary


class UTIForm(ModelForm):
    class Meta:
        pass
    
class DescriptionForm(UTIForm):
    class Meta:
        model=Description
        exclude=('desc_type','desc_object','originator','created_date','object_id')
        
class SummaryForm(UTIForm):
    class Meta:
        model=Summary
        exclude=('summ_type','summ','originator','created_date','object_id')