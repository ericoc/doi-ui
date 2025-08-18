from datetime import date, datetime
from logging import getLogger


# Logger.
logger = getLogger(__name__)


def parse_date(item):
    """
    Parse "date-time" or "date-parts" chunks from DOI JSON.
    """
    if item:

        # "date-time" is likely ISO.
        iso_date = item.get("date-time")
        if iso_date:
            try:
                return datetime.fromisoformat(iso_date)
            except ValueError as iso_date_err:
                logger.exception(iso_date_err)
                pass

        # "date-parts" is likely three-part dictionary of [[year, month, day]].
        date_parts = item.get("date-parts")
        if date_parts:
            try:
                p_date = date_parts[0]
                if p_date:
                    year = p_date[0]
                    month = p_date[1] or 1
                    day = p_date[2] or 1
                    return date(int(year), int(month), int(day))
            except TypeError as date_parts_err:
                logger.exception(date_parts_err)
                pass
            return date_parts

        return item
    return None
