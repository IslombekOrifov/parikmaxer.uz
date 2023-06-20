from uuid import uuid4
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators

from accounts.models import (
    CustomUser, 
    Profile, 
    Experience, 
    News
)


class UserRegisterSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(
        required=True, validators=[validators.UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            custom_id = str(uuid4())[-12:]
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['is_staff', 'is_active', 'date_joined', 'custom_id', 'is_worker', 'is_company', 'is_deleted']

    def validate_email(self, value):
        print()
        print()
        print(value)
        print()
        print()
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError({"email": "Email already in use."})
        return value
    

class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user',]

    
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        exclude = ['user', 'created_at']


# class NewsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = News
#         fields = "__all__"
#         extra_kwargs = {
#             'slug': {'read_only': True},
#             'created_at': {'read_only': True},
#             'updated_at': {'read_only': True},
#             'author': {'read_only': True},
#             'status': {'write_only': True},
#             'is_deleted': {'write_only': True},
#         }
    
#     def create(self, validated_data):
#         validated_data['slug']=str(uuid4())[-20:]
#         return super().create(self, validated_data)
    