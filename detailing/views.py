import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate, TruncWeek
from django.views.generic import DetailView, ListView
from datetime import timedelta
from django.utils.timezone import now
from .models import Job, ServiceTransition
from dateutil.relativedelta import relativedelta



# Create your views here.
class UserServiceTrackerView(DetailView):
    model = Job
    template_name = r'detailing/user_job_detailing.html'
    context_object_name = 'job'

    def get_object(self, **kwargs):
        # Получаем UUID задания из URL
        job_id = self.kwargs.get('job_id')
        return Job.objects.prefetch_related(
            'car',
            'service',
            'transitions__status',
        ).get(id=job_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()

        # Формирование контекста
        context['car'] = job.car
        context['client'] = job.client
        context['service'] = job.service
        context['price'] = job.service.price
        context['transitions'] = job.transitions.all()
        context['photos'] = [transition.photo.url for transition in job.transitions.all() if transition.photo]
        return context

class DashboardView(ListView):
    model = Job
    template_name = r'dashboard/dashboard.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        period = self.request.GET.get('period', '')
        job_status = self.request.GET.get('job_status', '')

        queryset = Job.objects.select_related('client', 'car', 'service').order_by('-created_at')

        # Фильтрация по времени
        if period == 'today':
            queryset = queryset.filter(created_at__date=now().date())
        elif period == 'last_week':
            start_date = now().date() - timedelta(days=7)
            queryset = queryset.filter(created_at__date__gte=start_date)
        elif period == 'last_month':
            first_day_last_month = now() - relativedelta(months=1)
            first_day_last_month = first_day_last_month.replace(day=1)
            queryset = queryset.filter(created_at__date__gte=first_day_last_month)
        elif period == 'last_year':
            first_day_last_year = now().replace(month=1, day=1) - relativedelta(years=1)
            queryset = queryset.filter(created_at__date__gte=first_day_last_year)

        # Фильтрация по статусу
        if job_status:
            queryset = queryset.filter(job_status=job_status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        period = self.request.GET.get('period', '')

        # Данные для группировки по неделям
        weekly_data = Job.objects.annotate(week=TruncWeek('created_at')) \
                                  .values('week') \
                                  .annotate(total_jobs=Count('id')) \
                                  .order_by('-week')

        formatted_weekly_data = []
        for entry in weekly_data:
            week_start = entry['week']
            week_end = week_start + timedelta(days=6)
            formatted_weekly_data.append({
                'week': f"{week_start.strftime('%d %B')} - {week_end.strftime('%d %B')}",
                'week_start': week_start.strftime('%Y-%m-%d'),
                'week_end': week_end.strftime('%Y-%m-%d'),
                'total_jobs': entry['total_jobs']
            })

        context['weekly_data'] = formatted_weekly_data

        # Данные для графиков
        revenue_data = Job.objects.select_related('service')
        if period == 'today':
            revenue_data = revenue_data.filter(created_at__date=now().date())
        elif period == 'last_week':
            start_date = now().date() - timedelta(days=7)
            revenue_data = revenue_data.filter(created_at__date__gte=start_date)
        elif period == 'last_month':
            first_day_last_month = now() - relativedelta(months=1)
            first_day_last_month = first_day_last_month.replace(day=1)
            revenue_data = revenue_data.filter(created_at__date__gte=first_day_last_month)
        elif period == 'last_year':
            first_day_last_year = now().replace(month=1, day=1) - relativedelta(years=1)
            revenue_data = revenue_data.filter(created_at__date__gte=first_day_last_year)

        revenue_aggregated = revenue_data.annotate(date=TruncDate('created_at')) \
                                         .values('date') \
                                         .annotate(total_revenue=Sum('service__price')) \
                                         .order_by('date')

        context['revenue_chart_data'] = json.dumps(list(revenue_aggregated), cls=DjangoJSONEncoder)

        job_data = Job.objects.all()
        if period == 'today':
            job_data = job_data.filter(created_at__date=now().date())
        elif period == 'last_week':
            start_date = now().date() - timedelta(days=7)
            job_data = job_data.filter(created_at__date__gte=start_date)
        elif period == 'last_month':
            first_day_last_month = now() - relativedelta(months=1)
            first_day_last_month = first_day_last_month.replace(day=1)
            job_data = job_data.filter(created_at__date__gte=first_day_last_month)
        elif period == 'last_year':
            first_day_last_year = now().replace(month=1, day=1) - relativedelta(years=1)
            job_data = job_data.filter(created_at__date__gte=first_day_last_year)

        job_aggregated = job_data.annotate(date=TruncDate('created_at')) \
                                   .values('date') \
                                   .annotate(job_count=Count('id')) \
                                   .order_by('date')

        context['job_chart_data'] = json.dumps(list(job_aggregated), cls=DjangoJSONEncoder)

        return context

