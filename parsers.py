from datetime import date, datetime
from logging import getLogger


# Logging.
logger = getLogger(__name__)


def parse_date(item):
    """
    Parse "date-time" and "date-parts" chunks from DOI JSON.
    """
    if item:

        # ISO date.
        iso_dt = item.get("date-time")
        if iso_dt:
            try:
                return datetime.fromisoformat(iso_dt)
            except ValueError as iso_dt_val_err:
                logger.error(f"Failed parsing ISO date: {item}")
                logger.exception(iso_dt_val_err)

        # Three-part (year, month, day) dictionary of "date-parts".
        date_parts = item.get("date-parts")
        if date_parts:
            try:
                date_parts = date_parts[0]
                year = date_parts[0]
                month = date_parts[1] or 1
                day = date_parts[2] or 1
                return date(year, month, day)
            except IndexError as date_parts_idx_err:
                logger.error(f"Failed to parse date parts: {item}")
                logger.exception(date_parts_idx_err)

        return item

    return None
