from django import template
from datetime import date, timedelta
from .. import models

register = template.Library()


@register.filter(name="is_rushorder")
def is_rushorder(order):
    return order.due-order.arrival <= models.Constants.rush_order_days


@register.filter(name='get_date_str')
def get_date_str(day,today):
    delta = day - today

    if delta == 0:
        return "Heute!"
    elif delta < 1:
        return "vor %s %s" % (abs(delta),
            ("Tag" if abs(delta) == 1 else "Tagen"))
    elif delta == 1:
        return "Morgen!"
    elif delta > 1:
        return "In %s Tagen" % delta


@register.filter(name='get_date')
def get_date(day):

    return date.today() + timedelta(day) # -timedelta(days=delta)
