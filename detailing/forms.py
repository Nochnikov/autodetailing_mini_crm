from django import forms
from detailing.models import *


class ServiceTransitionForm(forms.ModelForm):
    class Meta:
        model = ServiceTransition
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Если мы работаем с существующей записью
        if self.instance and self.instance.job:
            # Получаем все сервисы, связанные с этой задачей через ServiceTransition
            related_services = ServiceTransition.objects.filter(job=self.instance.job).values_list('service_id',
                                                                                                   flat=True).distinct()

            # Фильтруем статусы, связанные с этими сервисами
            self.fields['status'].queryset = Status.objects.filter(service_id__in=related_services)
        else:
            # Если Job ещё не задан, показываем пустой QuerySet
            self.fields['status'].queryset = Status.objects.none()


