from datetime import date, datetime


def isfuture(when: (date, datetime, None) = None) -> bool:
    """Boolean whether a date or datetime is in the future."""
    ret = False
    try:
        if isinstance(when, datetime):
            when = when.date()
        if date.today() <= when:
            ret = True
    except TypeError:
        pass
    return ret


def prettytime(when: (date, datetime, str, None) = None) -> str:
    """Format date and datetime, as needed, for Jinja2."""
    if when:
        if isinstance(when, date):
            return when.strftime("%A, %B %d, %Y")
        if isinstance(when, datetime):
            return when.strftime("%A, %B %d, %Y @ %H:%M:%S %z (%Z)")
    return str(when)
