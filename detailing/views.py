from django.views.generic import DetailView, ListView
from detailing.models import Category
from datetime import timedelta
from django.utils.timezone import now


# Create your views here.
class UserServiceTrackerView(DetailView):
    model = Category
    template_name = r'detailing/user_category_detailing.html'
    # form_class = GetUserCategoryForm
    context_object_name = 'field'


    def get_object(self, **kwargs):
        category_id = self.kwargs.get('category_id')
        return Category.objects.get(id=category_id)



class DashboardView(ListView):
    model = Category
    template_name = r'dashboard/dashboard.html'
    context_object_name = 'categories'

    def get_queryset(self):
        period = self.request.GET.get('period', 'all')
        queryset = Category.objects.select_related('client', 'car', 'status').all()

        today = now().date()

        if period == 'today':
            # Фильтрация по текущему дню
            return queryset.filter(created_at__date=today)

        elif period == 'last_week':
            # Начало и конец прошлой недели
            start_date = today - timedelta(days=today.weekday() + 7)  # Понедельник прошлой недели
            end_date = today - timedelta(days=today.weekday() + 1)   # Воскресенье прошлой недели
            return queryset.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)

        elif period == 'last_month':
            # Определяем начало и конец прошлого месяца
            first_day_of_this_month = today.replace(day=1)
            last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
            start_date = last_day_of_last_month.replace(day=1)
            return queryset.filter(created_at__date__gte=start_date, created_at__date__lte=last_day_of_last_month)

        elif period == 'last_year':
            start_date = today.replace(year=today.year - 1, month=1, day=1)
            end_date = today.replace(year=today.year - 1, month=12, day=31)
            return queryset.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        return context

