from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import JobListCreateView, JobDetailView
from .views import ApplyToJobView, ListApplicationsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns += [
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:id>/', JobDetailView.as_view(), name='job-detail'),
]

urlpatterns += [
    path('jobs/<int:id>/apply/', ApplyToJobView.as_view(), name='job-apply'),
    path('applications/', ListApplicationsView.as_view(), name='my-applications'),
]