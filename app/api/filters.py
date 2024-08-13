from django.db.models import Q
from django_filters import rest_framework as filters


class PostFilter(filters.FilterSet):
    search = filters.CharFilter(method="search_text")

    def search_text(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(content__icontains=value)
        )
