from django.db.models import Q

from django_filters import rest_framework as filters


class PostFilter(filters.FilterSet):
    """Класс фильтра для модели Post"""

    # Определяем поле фильтра 'search', которое принимает строку для поиска
    # Указываем, что для фильтрации используется пользовательский метод 'search_text'
    search = filters.CharFilter(method="search_text")

    # Метод для пользовательской фильтрации на основе текста поиска
    def search_text(self, queryset, name, value):
        # Фильтруем queryset, используя оператор Q для поиска по частичному совпадению текста
        # Осуществляется поиск по полям 'title' и 'content', независимо от регистра
        return queryset.filter(Q(title__icontains=value) | Q(content__icontains=value))
