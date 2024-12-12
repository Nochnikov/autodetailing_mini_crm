from django.db.models import Prefetch
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
            'transitions__service',
            'transitions__status'
        ).get(id=job_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()

        context['car'] = job.car
        context['client'] = job.client
        context['services'] = {transition.service for transition in job.transitions.all()}
        context['transitions'] = job.transitions.all()
        context['photos'] = [transition.photo.url for transition in job.transitions.all() if transition.photo]

        return context


class DashboardView(ListView):
    model = Job
    template_name = r'dashboard/dashboard.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        period = self.request.GET.get('period', 'all')

        queryset = Job.objects.select_related('client', 'car').prefetch_related(
            Prefetch(
                'transitions',  # Поле related_name в ServiceTransition
                queryset=ServiceTransition.objects.select_related('service'),  # Предварительная загрузка service
            )
        )
        # Фильтруем данные
        if period == 'today':
            return queryset.filter(created_at__date=now().date())
        elif period == 'last_week':
            start_date = now().date() - timedelta(days=7)
            return queryset.filter(created_at__date__gte=start_date)
        elif period == 'last_month':
            start_date = now().date() - timedelta(days=30)
            return queryset.filter(created_at__date__gte=start_date)
        elif period == 'last_year':
            start_date = now() - relativedelta(years=1)
            return queryset.filter(created_at__date__gte=start_date)
        return queryset