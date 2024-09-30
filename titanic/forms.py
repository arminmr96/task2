from django import forms
from titanic.models import TitanicPassenger

class TitanicPassengerForm(forms.ModelForm):
    passenger_id = forms.CharField()
    
    class Meta:
        model = TitanicPassenger
        fields = "__all__"
