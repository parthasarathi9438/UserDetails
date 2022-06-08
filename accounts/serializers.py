from pyexpat import model
from attr import fields
from rest_framework import serializers
from django.contrib.auth.models import User

from accounts.models import Account



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user
class AccountSerializer(serializers.ModelSerializer):
    user_one = UserSerializer(source='user', read_only=True)
    class Meta:
        model = Account
        fields = ['user','phone', 'description', 'date_of_birth','gender','profile_picture','created_on','updated_on', 'user_one']

class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']

        old_password = serializers.CharField(required=True)
        new_password = serializers.CharField(required=True)