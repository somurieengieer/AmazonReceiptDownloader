import re

# return url path e.q. http://aaa/bbb/ccc.py -> http://aaa/bbb/
def get_url_path(url):
    return re.sub('/[^/]*$', '/', url)

# return Date (format is YYYYMMDD)
def pickDate(date):
    pattern = re.compile('([0-9]{4})年([0-9]{1,2})月([0-9]{1,2})日')
    result = pattern.search(date)
    if result:
        y, m, d = result.groups()
        return y + '{:02}'.format(int(m)) + '{:02}'.format(int(d))
    else:
        return None
