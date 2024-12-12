from django import forms
from detailing.models import *


class ServiceTransitionForm(forms.ModelForm):
    class Meta:
        model = ServiceTransition
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields['status'].queryset = Status.objects.filter(service_id=self.instance.service_id)
        else:
            self.fields['status'].queryset = Status.objects.none()


