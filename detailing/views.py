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
          # Добавим связь с сервисом для получения информации о сервисе
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

        queryset = Job.objects.select_related('client', 'car', 'service')

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

        # Фильтрация по статусу (проверяем, задан ли статус)
        if job_status:
            queryset = queryset.filter(job_status=job_status)

        return queryset
