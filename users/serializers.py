from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken

def create_member(validated_data):
    member_data = validated_data.pop('member')
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
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = ('auth_user', 'contact_no', 'member_type', 'city', 'address', 'profile_pic', 'access', 'refresh')

    def get_access(self, obj):
        refresh = RefreshToken.for_user(obj.auth_user)
        return str(refresh.access_token)

    def get_refresh(self, obj):
        refresh = RefreshToken.for_user(obj.auth_user)
        return str(refresh)

class IndividualRegisterSerializer(serializers.ModelSerializer):

    member = MemberSerializer()
    ngo_static_id = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = Individual
        fields = ('member', 'name', 'is_volunteer', 'id_number', 'ngo_static_id')

    def create(self, validated_data):
        ngo = None
        if validated_data['is_volunteer']:
            if not 'ngo_static_id' in validated_data and not 'id_number' in validated_data:
                raise ValidationError("Please provide all details.")
            ngo_qs = NGO.objects.filter(member__static_id=validated_data.pop('ngo_static_id'))
            if ngo_qs.exists():
                ngo = ngo_qs[0]
            else:
                raise ValidationError("No such NGO registered.")
        member = create_member(validated_data)
        individual = Individual.objects.create(member=member, ngo=ngo, **validated_data)
        return individual

class RestaurantRegisterSerializer(serializers.ModelSerializer):

    member = MemberSerializer()

    class Meta:
        model = Restaurant
        fields = '__all__'

    def create(self, validated_data):
        member = create_member(validated_data)
        restaurant = Restaurant.objects.create(member=member, **validated_data)
        return restaurant

class NGORegisterSerializer(serializers.ModelSerializer):

    member = MemberSerializer()

    class Meta:
        model = NGO
        fields = '__all__'

    def create(self, validated_data):
        member = create_member(validated_data)
        ngo = NGO.objects.create(member=member, **validated_data)
        return ngo

class MemberDetailSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = ('contact_no', 'member_type', 'profile_pic', 'address', 'city', 'name')

    def get_name(self, obj):
        return obj.get_name()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['city'] = City.objects.get(pk=data['city']).name
        data['profile_pic'] = instance.get_profile_pic_url()
        return data

class CityListSerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('name', )

class NGOListSerializer(serializers.ModelSerializer):

    static_id = serializers.SerializerMethodField()

    class Meta:
        model = NGO
        fields = ('name', 'static_id')

    def get_static_id(self, obj):
        return obj.member.static_id

    