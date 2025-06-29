from datetime import date, datetime


def parse_date(item: (dict, None)) -> (date, datetime, None):
    """
    Parse "date-time" and "date-parts" chunks from DOI JSON.
    """
    if item:
        iso_dt = item.get("date-time")
        if iso_dt:
            try:
                return datetime.fromisoformat(iso_dt)
            except ValueError:
                pass

        date_parts = item.get("date-parts")
        if date_parts:
            p_date = date_parts[0] or None
            if p_date:
                year = p_date[0] or None
                month = p_date[1] or 1
                day = p_date[2] or 1
                if year:
                    return date(year, month, day)

        return item

    return None
