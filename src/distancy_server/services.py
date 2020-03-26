from datetime import datetime


def read_dt_str(dt_str: str):
    """The standard datetime has trouble interpreting the Z"""
    if dt_str[-1] == 'Z':
        dt_str = dt_str[:-1]
        dt_str = dt_str + '+00:00'

    dt = datetime.fromisoformat(dt_str)
    return dt
