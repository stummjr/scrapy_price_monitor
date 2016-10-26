from datetime import datetime, timedelta


def timestamp_from_reversed(reversed):
    return datetime(5000, 1, 1) - timedelta(seconds=float(reversed))


def reversed_timestamp():
    return str((datetime(5000, 1, 1) - datetime.now()).total_seconds())
