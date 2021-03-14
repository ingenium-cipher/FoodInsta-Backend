from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.validators import UniqueValidator


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs


class UserRegisterSerializer(serializers.ModelSerializer):

    auth_user = UserSerializer()
    # contact_no = serializers.IntegerField(required=True, max_value=9999999999, min_value=1111111111, validators=[UniqueValidator(queryset=Member.objects.all())])

    class Meta:
        model = Member
        fields = ('auth_user', 'contact_no')

    def create(self, validated_data):
        user_data = validated_data.pop('auth_user')
        user_data.pop('password2')
        auth_user = User.objects.create(**user_data)
        auth_user.set_password(user_data['password'])
        auth_user.save()

        member = Member.objects.create(auth_user=auth_user, contact_no=validated_data['contact_no'])
        return member