from rest_framework import serializers
from .models import User
from .models import Job

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'user_type')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            user_type=validated_data.get('user_type', 'job_seeker'),
            password=validated_data['password']
        )
        return user
class JobSerializer(serializers.ModelSerializer):
    employer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['employer', 'created_at']