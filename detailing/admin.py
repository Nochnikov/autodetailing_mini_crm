from django.contrib import admin
from detailing.models import *
from .forms import *

# Register your models here.

class ServiceTransitionInline(admin.TabularInline):
    model = ServiceTransition
    fields = ('service', 'status', 'photo', 'changed_at')
    readonly_fields = ('changed_at',)
    extra = 0

class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'car', 'get_services_list', 'job_status', 'created_at')
    inlines = [ServiceTransitionInline]

    def get_services_list(self, obj):
        return ", ".join([service.name for service in obj.get_services()])
    get_services_list.short_description = "Services"



admin.site.register(Job, JobAdmin)
admin.site.register(Service)
admin.site.register(ServiceTransition)
admin.site.register(Car)
admin.site.register(Status)
admin.site.register(Client)
