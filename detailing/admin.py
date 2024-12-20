from detailing.models import *
# Register your models here.
from django.contrib import admin
from .models import Job, ServiceTransition, Status


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


class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'car', 'service', 'job_status', 'created_at')
    inlines = [ServiceTransitionInline]  # Инлайн для переходов статуса
    search_fields = ('id', 'client__name', 'car__license_plate')




admin.site.register(Job, JobAdmin)
admin.site.register(ServiceTransition)
admin.site.register(Car)
admin.site.register(Status)
admin.site.register(Client)

admin.site.site_header = 'Lucent Car'
admin.site.site_title = 'Lucent Car Admin'
admin.site.index_title = 'Welcome to Lucent Car Administration'


