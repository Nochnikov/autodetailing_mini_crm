from django.contrib import admin
from .models import ServiceTransition, Status


class ServiceTransitionInline(admin.TabularInline):
    model = ServiceTransition
    extra = 0
    fields = ('status', 'photo', 'changed_at')
    readonly_fields = ('changed_at',)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            formset.form.base_fields['status'].queryset = Status.objects.filter(service=obj.service)
        return formset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        job = self.instance.job if hasattr(self, 'instance') else None
        if db_field.name == 'status' and job:
            kwargs['queryset'] = Status.objects.filter(service=job.service)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class ServiceStatusInline(admin.TabularInline):
    model = Status
    extra = 0
    fields = ['name_of_the_status', 'description_of_the_status']
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            formset.form.base_fields['name_of_the_status'].queryset = Status.objects.filter(service=obj)
        return formset
