from datetime import date, datetime


def isfuture(when: (date, datetime, None) = None) -> bool:
    """Boolean whether a (publshed) date or datetime is in the future."""
    if isinstance(when, datetime):
        when = when.date()
    if date.today() <= when:
        return True
    return False


def prettytime(when: (date, datetime, str, None) = None) -> str:
    """Format date and datetime, as needed, for Jinja2."""
    if isinstance(when, date):
        return when.strftime("%A, %B %d, %Y")
    if isinstance(when, datetime):
        return when.strftime("%A, %B %d, %Y @ %H:%M:%S %z (%Z)")
    return str(when)
