from rest_framework.decorators import action
from rest_framework.response import Response

class CountModelMixin(object):
    """
    Count a mocel viewset queryset.
    Cite: https://stackoverflow.com/a/49709157/9708266
    """

    def get_count(self, queryset):
        return queryset.count()

    @action(detail=False, methods=['get'])
    def count(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        content = {'count': queryset.count()}
        return Response(content)
