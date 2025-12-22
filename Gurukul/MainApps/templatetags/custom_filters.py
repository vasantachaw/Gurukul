from django import template
from django.utils.timesince import timesince
register = template.Library()


@register.filter
def first_word(value):
    value=str(value).strip()
    return value.split()[0] if value.split() else ''




@register.filter
def humanize_number(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return value

    if value >= 1000000:
        return f"{value/1000000:.1f}M"
    elif value >= 1000:
        return f"{value/1000:.1f}k"
    else:
        return str(value)
    

@register.filter
def time_since_simple(value):
    if not value:
        return ""
    time_str = timesince(value).split(',')[0]
    number, unit = time_str.split()  # Split "2 hours" -> ["2", "hours"]
    
    # Map full units to short forms
    unit_map = {
        'years': 'y',
        'year': 'y',
        'months': 'mo',
        'month': 'mo',
        'weeks': 'w',
        'week': 'w',
        'days': 'd',
        'day': 'd',
        'hours': 'h',
        'hour': 'h',
        'minutes': 'm',
        'minute': 'm',
        'seconds': 's',
        'second': 's',
    }
    
    short_unit = unit_map.get(unit, unit)
    
    return f"{number}{short_unit} ago"


@register.filter
def format_duration(months):
    """
    Converts total months into 'X years Y months' format.
    Example: 5 -> '5 months', 13 -> '1 year 1 month', 24 -> '2 years'
    """
    try:
        months = int(months)
    except (TypeError, ValueError):
        return ""

    if months <= 12:
        return f"{months} month{'s' if months != 1 else ''}"
    else:
        years = months // 12
        remaining_months = months % 12
        if remaining_months == 0:
            return f"{years} year{'s' if years != 1 else ''}"
        else:
            return f"{years} year{'s' if years != 1 else ''} {remaining_months} month{'s' if remaining_months != 1 else ''}"


@register.filter
def mul(value, arg):
    return value * arg




@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0