from datetime import date, datetime


def parse_date(item: (dict, None)) -> (date, datetime, None):
    '''Parse "date-time" and "date-parts" chunks from DOI JSON.'''
    if item:
        iso_dt = item.get("date-time")
        if iso_dt:
            try:
                return datetime.fromisoformat(iso_dt)
            except ValueError:
                pass

        date_parts = item.get("date-parts")
        if date_parts:
            p_date = date_parts[0]
            if p_date:
                if len(p_date) == 3:
                    return date(p_date[0], p_date[1], p_date[2])
                elif len(p_date) == 2:
                    return date(p_date[0], p_date[1], 1)
                elif len(p_date) == 1 and p_date[0] is not None:
                    return date(p_date[0], 1, 1)
        return item

    return None
