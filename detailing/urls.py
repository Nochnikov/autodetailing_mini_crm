from django.urls import path
from detailing import views

urlpatterns = [
        path('<uuid:job_id>/', views.UserServiceTrackerView.as_view(), name='index'),
]
