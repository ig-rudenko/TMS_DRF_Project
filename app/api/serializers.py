import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.models import Post, Tag


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""

    class Meta:
        # Указываем модель, для которой создается сериализатор
        model = get_user_model()
        # Указываем поля, которые будут включены в сериализованный выходной результат
        fields = ['id', 'username', 'email']


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели поста"""

    # Определяем поле для тегов, используя SlugRelatedField для сериализации отношений с моделью Tag
    tags = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Tag.objects.all())
    # Определяем поле для пользователя, используя вложенный сериализатор UserSerializer
    user = UserSerializer(read_only=True)

    class Meta:
        # Указываем модель, для которой создается сериализатор
        model = Post
        # Указываем поля, которые будут включены в сериализованный выходной результат
        fields = ["id", 'title', 'content', "tags", "user", "short_content"]
        # Указываем поля, которые будут доступны только для чтения
        read_only_fields = ["id", "user", "short_content"]

    # Метод для валидации поля 'title'
    def validate_title(self, value: str) -> str:
        # Проверяем, начинается ли заголовок с цифры
        if re.match(r"^\d", value):
            # Если заголовок начинается с цифры, выбрасываем ошибку валидации
            raise ValidationError("Заголовок не должен начинаться с цифры")
        # Возвращаем валидное значение заголовка
        return value

    # Метод для общей валидации данных
    def validate(self, attrs):
        # Проверяем, совпадают ли значения заголовка и содержимого
        if attrs['title'] == attrs['content']:
            # Если заголовок совпадает с содержимым, выбрасываем ошибку валидации
            raise ValidationError("Заголовок не должен совпадать с текстом")
        # Возвращаем валидные атрибуты
        return attrs
