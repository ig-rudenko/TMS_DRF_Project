import re

from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.models import Post, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Tag.objects.all())
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", 'title', 'content', "tags", "user", "short_content"]
        read_only_fields = ["id", "user", "short_content"]

    def validate_title(self, value: str) -> str:
        if re.match(r"^\d", value):
            raise ValidationError("Заголовок не должен начинаться с цифры")
        return value

    def validate(self, attrs):
        if attrs['title'] == attrs['content']:
            raise ValidationError("Заголовок не должен совпадать с текстом")
        return attrs
