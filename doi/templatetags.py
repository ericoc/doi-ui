from datetime import date, datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.template.defaulttags import register
from django.utils.timesince import timesince, timeuntil


@register.filter(name="get_dict_item")
def get_dict_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name="human_time")
def human_time(when: (date, datetime)) -> str:

    current = None
    ret = str(when)
    fmt = "%A, %B %d, %Y"

    if isinstance(when, date):
        current = date.today()

    if isinstance(when, datetime):
        current = datetime.now().astimezone(tz=ZoneInfo(settings.TIME_ZONE))

    if current:
        ret = ""
        if when <= current:
            ret += f"{timesince(when)} ago"
        else:
            ret += f"in {timeuntil(when)}"

    return ret
