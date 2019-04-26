from django import forms
from .models import Bed

class BedForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ('bed_type', 'initial_num', 'num_used')