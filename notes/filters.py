import django_filters
from django_filters import DateFilter

from .models import Note

class NoteFilter(django_filters.FilterSet):

    CHOICES = (
        ('ascending', 'Ascending'),
        ('descending', 'Descending')
    )

    ordering = django_filters.ChoiceFilter(label = 'Ordering', choices = CHOICES, method = 'filter_by_order')

    start_created = DateFilter(field_name = "created", lookup_expr = 'gte')
    end_created = DateFilter(field_name = "created", lookup_expr = 'lte')
    start_updated = DateFilter(field_name = "updated", lookup_expr = 'gte')
    end_updated = DateFilter(field_name = "updated", lookup_expr = 'lte')

    class Meta :
        model = Note
        fields = '__all__'
        exclude = ['user', 'note', 'title', 'created', 'updated']

    def filter_by_order(self, queryset, name, value) :
        expression = 'created' if value == 'ascending' else '-created' 
        return queryset.order_by(expression)