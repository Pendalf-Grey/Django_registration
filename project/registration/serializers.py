from rest_framework import serializers
from .models import User, UserProfile
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Добавляем поле для пароля

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'phone_number')  # Поля для регистрации
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'phone_number': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
        )

        user.set_password(validated_data['password'])
        user.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        validated_data['access_token'] = access_token
        validated_data['refresh_token'] = str(refresh)

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.FileField(max_length=None, use_url=True, required=False)

    class Meta:
        model = UserProfile
        fields = ('avatar', 'description')
