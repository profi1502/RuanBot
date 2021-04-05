URL = 'http://www.google.com/maps?q={lat},+{lon}'


def show(lat, lon):
    return f'<a href="{URL.format(lat=lat, lon=lon)}">ВІДКРИТИ НА МАПІ</a>'
