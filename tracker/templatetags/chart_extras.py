import json
from decimal import Decimal
from django import template

register = template.Library()

@register.filter
def json_labels(summary):
    labels = [row.get('category__name', '') for row in summary]
    return json.dumps(labels)

@register.filter
def json_data(summary):
    data = []
    for row in summary:
        total = row.get('total', 0)
        if isinstance(total, Decimal):
            total = float(total)
        data.append(total)
    return json.dumps(data)
