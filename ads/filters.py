import django_filters
from django.db.models import Q

from .models import Ad


class AdFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter', label='Поиск')
    category = django_filters.ChoiceFilter(
        field_name='category',
        lookup_expr='iexact'
    )
    condition = django_filters.ChoiceFilter(
        field_name='condition',
        lookup_expr='iexact',
        choices=[("", "Все состояния"), ("new", "Новый"), ("used", "Б/У")]
    )

    class Meta:
        model = Ad
        fields = ['search', 'category', 'condition']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Ad.objects.order_by('category').values_list('category', flat=True).distinct()
        choices = [("", "Все категории")]
        choices.extend([(cat, cat) for cat in categories if cat])
        self.filters['category'].field.empty_label = None
        self.filters['category'].field.choices = choices

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )
