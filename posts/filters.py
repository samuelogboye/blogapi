import django_filters
from django.db.models import Q
from .models import Post

class PostFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all_fields')

    class Meta:
        model = Post
        fields = []

    def filter_by_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(content__icontains=value)
        )
