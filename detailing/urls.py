from django.urls import path
from detailing import views



urlpatterns = [
        path('service/<uuid:category_id>/', views.UserServiceTrackerView.as_view(), name='index'),
        path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]