import django_filters
from ..models import Background


class BackgroundFilter(django_filters.FilterSet):
    background_source = django_filters.CharFilter(field_name="source")

    class Meta:
        model = Background
        fields = [f.name for f in model._meta.fields if f.name != 'source']
        fields += ['background_source']