from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(
        queryset=User.objects.all(), message="This email already exits",
    )])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True, allow_null=False, allow_blank=False)

    token_key = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'confirm_password',
                  'email', 'token_key')
        extra_kwargs = {
            'first_name': {'required': True, 'allow_null': False, 'allow_blank': False},
            'last_name': {'required': True, 'allow_null': False, 'allow_blank': False},
        }

    def get_token_key(self, instance):
        if self.instance:
            token, created = Token.objects.get_or_create(user=instance)
            return token.key
        return None

    def validate(self, attrs):
        confirm_password = attrs.pop('confirm_password', None)
        password = attrs.get('password', None)
        if not password == confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Password not matched'})
        return attrs

    def create(self, validated_data):

        user = super().create(validated_data=validated_data)

        user.set_password(validated_data['password'])
        user.save()
        return user


class GetUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
