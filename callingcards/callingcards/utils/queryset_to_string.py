import json
from decimal import Decimal
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


def queryset_to_string(queryset, num_records=5):
    """
    Convert a queryset to a human-readable JSON string representation.

    Takes a queryset as input, selects the first five records, and converts
    them to a JSON string with indentation for readability.

    Args:
        queryset: A Django queryset object.
        num_records: The number of records to include in the JSON string. 
          Default is 5.

    Returns:
        A human-readable JSON string representation of the queryset.
    """
    records = queryset.all()[:num_records]

    if records and isinstance(records[0], dict):
        # If the records are dictionaries/ordered dictionaries
        return json.dumps(list(records), indent=4, cls=CustomJSONEncoder)
    else:
        # If the records are model instances
        serialized_data = serialize('json', records)
        json_data = json.loads(serialized_data)
        return json.dumps(json_data, indent=4)
