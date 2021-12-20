from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields =  ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )
        return user

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]