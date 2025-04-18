from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import RegisterSerializer
from rest_framework import generics, permissions
from .models import Job
from .serializers import JobSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Application
from .models import Job
from .serializers import ApplicationSerializer


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
   

class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return []

    def perform_create(self, serializer):
        if self.request.user.user_type != 'employer':
            raise PermissionError("Only employers can post jobs.")
        serializer.save(employer=self.request.user)


class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'id'
 

class ApplyToJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = request.user
        if user.user_type != 'job_seeker':
            return Response({'error': 'Only job seekers can apply for jobs.'}, status=403)

        job = get_object_or_404(Job, id=id)
        if Application.objects.filter(job=job, applicant=user).exists():
            return Response({'error': 'You have already applied to this job.'}, status=400)

        cover_letter = request.data.get('cover_letter', '')
        application = Application.objects.create(job=job, applicant=user, cover_letter=cover_letter)
        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=201)


class ListApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user).order_by('-created_at')


