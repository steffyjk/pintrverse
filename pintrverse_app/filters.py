from django_filters import FilterSet, CharFilter
from users.models import User
from pintrverse_app.models import Pin
from django.db.models import Q


class UserFilterSet(FilterSet):
    username = CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username', ]


class PinFilterSet(FilterSet):
    search_pin = CharFilter(method='filter_pins')

    def filter_pins(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(about__icontains=value) |
            Q(tag__name__icontains=value) |
            Q(user__username__icontains=value)
        )

    class Meta:
        model = Pin
        fields = ['search_pin']
