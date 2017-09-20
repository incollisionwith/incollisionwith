def indexed(row, name):
    value = int(row[name])
    if value != -1:
        return value


def sex_indexed(row, name):
    value = int(row[name])
    if value in (1, 2):
        return value

