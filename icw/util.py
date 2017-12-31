def indexed(row, name):
    value = int(row[name])
    if value != -1:
        return value


def sex_indexed(row, name):
    value = int(row[name])
    if value in (1, 2):
        return value

def other_page_url(request, page_num):
    query = request.GET.copy()
    if 'page' in query:
        query.pop('page')
    query.update({'page': page_num})
    return '?' + query.urlencode()

