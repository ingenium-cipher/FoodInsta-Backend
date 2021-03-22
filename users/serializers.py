from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('email',)


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
        email = member_data.pop('auth_user')['email']
        username = email.split('@')[0]
        auth_user = User.objects.create(email=email, username=username)
        auth_user.set_password(username + '@123')
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
        email = member_data.pop('auth_user')['email']
        username = email.split('@')[0]
        auth_user = User.objects.create(email=email, username=username)
        auth_user.set_password(username + '@123')
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
        email = member_data.pop('auth_user')['email']
        username = email.split('@')[0]
        auth_user = User.objects.create(email=email, username=username)
        auth_user.set_password(username + '@123')
        auth_user.save()

        member = Member.objects.create(auth_user=auth_user, **member_data)
        ngo = NGO.objects.create(member=member, **validated_data)
        return  ngo

    