from rest_framework import serializers
import re

from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'name',
            'email',
            'password',
            'password_confirm',
            'created_at',
        ]
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "Parol kamida 6 ta belgidan iborat bo'lishi kerak."
            )
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                "Parolda kamida bitta katta harf (A-Z) bo'lishi kerak."
            )
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(
                "Parolda kamida bitta kichik harf (a-z) bo'lishi kerak."
            )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/`~;]', value):
            raise serializers.ValidationError(
                "Parolda kamida bitta maxsus belgi (!@#$% va h.k.) bo'lishi kerak."
            )
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': "Parollar mos kelmadi."
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        return CustomUser.objects.create_user(
            password=password,
            **validated_data
        )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'name',
            'email',
            'balance',
            'role',
            'created_at',
        ]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['name', 'current_password', 'new_password', 'confirm_password']

    def validate(self, attrs):
        current_password = attrs.get("current_password")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        # agar user parolni o‘zgartirmoqchi bo‘lsa
        if current_password or new_password or confirm_password:
            if not current_password:
                raise serializers.ValidationError("Eski parol kiritilishi kerak.")

            user = self.instance
            if not user.check_password(current_password):
                raise serializers.ValidationError("Eski parol noto‘g‘ri.")

            if not new_password:
                raise serializers.ValidationError("Yangi parol kiritilishi kerak.")

            if new_password != confirm_password:
                raise serializers.ValidationError("Yangi parollar mos emas.")

        return attrs

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)

        new_password = validated_data.get("new_password")
        if new_password:
            instance.set_password(new_password)

        instance.save()
        return instance

