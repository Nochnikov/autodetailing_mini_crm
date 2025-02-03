# Register your models here.

from detailing.models import *
from django.contrib import admin
from .models import Job, ServiceTransition, Status, Service, WhatsAppNewsletter
from rangefilter.filters import DateRangeFilter
from .inlines import ServiceTransitionInline

class JobAdmin(admin.ModelAdmin):
    list_display = ('car', 'service', 'job_status', 'created_at', 'job_started', 'client',)
    inlines = [ServiceTransitionInline]
    search_fields = ('id', 'client__first_name', "client__last_name", "job_status", 'car__car_number')
    list_filter = [
        ("created_at", DateRangeFilter),
        ("job_started", DateRangeFilter)
    ]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price']
    # inlines = [ServiceStatusInline]
    search_fields = ("name", "price")


admin.site.register(Job, JobAdmin)
admin.site.register(ServiceTransition)
admin.site.register(Car)
admin.site.register(Status)
admin.site.register(Client)
admin.site.register(Service, ServiceAdmin)
admin.site.register(WhatsAppNewsletter)

admin.site.site_header = 'Lucent Car'
admin.site.site_title = 'Lucent Car Admin'
admin.site.index_title = 'Welcome to Lucent Car Administration'
