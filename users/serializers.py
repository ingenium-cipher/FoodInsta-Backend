from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

def create_member(validated_data):
    member_data = validated_data.pop('member')
    print(member_data)
    city_name = member_data.pop('city')
    city = City.objects.filter(name__iexact = city_name)
    if not city.exists():
        raise ValidationError("Enter a valid city")
    email = member_data.pop('auth_user')['email']
    username = email.split('@')[0]
    auth_user = User.objects.create(email=email, username=username)
    auth_user.set_password(username + '@123')
    auth_user.save()

    return Member.objects.create(auth_user=auth_user, city = city[0], **member_data)

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('email',)


class MemberSerializer(serializers.ModelSerializer):

    auth_user = UserSerializer()
    city = serializers.CharField(max_length=50)
    
    class Meta:
        model = Member
        fields = ('auth_user', 'contact_no', 'member_type', 'city', 'address', 'profile_pic')

class IndividualRegisterSerializer(serializers.ModelSerializer):

    member = MemberSerializer()

    class Meta:
        model = Individual
        fields = '__all__'

    def create(self, validated_data):
        member = create_member(validated_data)
        individual = Individual.objects.create(member=member, **validated_data)
        return individual

class RestaurantRegisterSerializer(serializers.ModelSerializer):

    member = MemberSerializer()

    class Meta:
        model = Restaurant
        fields = '__all__'

    def create(self, validated_data):
        member = create_member(validated_data)
        restaurant = Restaurant.objects.create(member=member, **validated_data)
        return  restaurant

class NGORegisterSerializer(serializers.ModelSerializer):

    member = MemberSerializer()

    class Meta:
        model = NGO
        fields = '__all__'

    def create(self, validated_data):
        member = create_member(validated_data)
        ngo = NGO.objects.create(member=member, **validated_data)
        return  ngo

    