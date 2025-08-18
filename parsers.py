from datetime import date, datetime, timezone
from logging import getLogger


# Logging.
logger = getLogger(__name__)


def parse_date(item):
    """
    Parse "timestamp", "date-time", or "date-parts" DOI date/time information.
    """
    if item:

        # UNIX/epoch timestamp (in milliseconds).
        #   Example: { "timestamp": 1753880563838 }
        timestamp = item.get("timestamp")
        if timestamp:
            timestamp = timestamp / 1000
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)

        # ISO date.
        #   Example: { "date-time": "2025-07-30T13:02:43Z" }
        iso_dt = item.get("date-time")
        if iso_dt:
            try:
                return datetime.fromisoformat(iso_dt)
            except ValueError as iso_dt_val_err:
                logger.error(f"Failed parsing ISO date: {item}")
                logger.exception(iso_dt_val_err)

        # Three-part nested list (year, month, day) in "date-parts" dictionary.
        #   Example: { "date-parts": [ [2025, 7, 1] ] }
        date_parts_out = item.get("date-parts")
        if date_parts_out:
            date_parts = date_parts_out[0]

            # "date-parts" dictionary always has year, but not month/day.
            if date_parts:
                year = date_parts[0]

                # Month.
                try:
                    month = date_parts[1]
                except IndexError:
                    month = 1

                # Day.
                try:
                    day = date_parts[2]
                except IndexError:
                    day = 1

                return date(year, month, day)

        return item

    return None
