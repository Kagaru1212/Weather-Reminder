from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def validate_email(self, value):
        if self.instance and self.instance.email != value:
            raise serializers.ValidationError("Изменение email запрещено.")
        return value
