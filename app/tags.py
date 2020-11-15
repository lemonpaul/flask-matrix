import jinja2


def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)


jinja2.environment.filters['datetimeformat'] = datetimeformat
