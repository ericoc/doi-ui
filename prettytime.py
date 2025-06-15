from datetime import date, datetime


def prettytime(when: (date, datetime, str, None) = None):
    """Format date and datetime, as needed, for Jinja2."""
    if isinstance(when, date):
        return when.strftime("%A, %B %d, %Y")
    if isinstance(when, datetime):
        return when.strftime("%A, %B %d, %Y @ %H:%M:%S %z (%Z)")
    return when
