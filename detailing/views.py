from datetime import timedelta
from django.utils.timezone import now
from django.views.generic import DetailView, ListView
from detailing.models import Category


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

        if period == 'today':
            return queryset.filter(created_at__date=now().date())
        elif period == 'last_week':
            start_date = now().date() - timedelta(days=7)
            return queryset.filter(created_at__date__gte=start_date)
        elif period == 'last_month':
            start_date = now().date() - timedelta(days=30)
            return queryset.filter(created_at__date__gte=start_date)
        elif period == 'last_year':
            start_date = now().date() - timedelta(days=365)
            return queryset.filter(created_at__date__gte=start_date)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        return context

