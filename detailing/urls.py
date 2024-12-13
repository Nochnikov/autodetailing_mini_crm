from django.conf.urls.static import static
from django.urls import path
from detailing import views
from mysite import settings

urlpatterns = [
        path('service/<uuid:job_id>/', views.UserServiceTrackerView.as_view(), name='index'),
        path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
