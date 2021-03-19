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
    email = serializers.EmailField(required=False, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs


class MemberSerializer(serializers.ModelSerializer):

    auth_user = UserSerializer()
    
    class Meta:
        model = Member
        fields = ('auth_user', 'contact_no', 'member_type')

class IndividualRegisterSerializer(serializers.ModelSerializer):

    member = MemberSerializer()

    class Meta:
        model = Individual
        fields = '__all__'

    def create(self, validated_data):
        member_data = validated_data.pop('member')
        user_data = member_data.pop('auth_user')
        user_data.pop('password2')
        auth_user = User.objects.create(**user_data)
        auth_user.set_password(user_data['password'])
        auth_user.save()

        member = Member.objects.create(auth_user=auth_user, **member_data)
        individual = Individual.objects.create(member=member, **validated_data)
        return individual

class RestaurantRegisterSerializer(serializers.ModelSerializer):

    member = MemberSerializer()

    class Meta:
        model = Restaurant
        fields = '__all__'

    def create(self, validated_data):
        member_data = validated_data.pop('member')
        user_data = member_data.pop('auth_user')
        user_data.pop('password2')
        auth_user = User.objects.create(**user_data)
        auth_user.set_password(user_data['password'])
        auth_user.save()

        member = Member.objects.create(auth_user=auth_user, **member_data)
        restaurant = Restaurant.objects.create(member=member, **validated_data)
        return  restaurant

class NGORegisterSerializer(serializers.ModelSerializer):

    member = MemberSerializer()

    class Meta:
        model = NGO
        fields = '__all__'

    def create(self, validated_data):
        member_data = validated_data.pop('member')
        user_data = member_data.pop('auth_user')
        user_data.pop('password2')
        auth_user = User.objects.create(**user_data)
        auth_user.set_password(user_data['password'])
        auth_user.save()

        member = Member.objects.create(auth_user=auth_user, **member_data)
        ngo = NGO.objects.create(member=member, **validated_data)
        return  ngo

    