import requests


def get_city(latitude, longitude):
    request_url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{longitude},{latitude}.' \
                  f'json?access_token=' \
                  f'pk.eyJ1IjoiZGRlYnVnZ2VyIiwiYSI6ImNrMTE1eWl6dzA1OGMzbnM4eHl3Y2xlbGEifQ.etdOh29HVSgDXq4wFoDEow' \
                  f'&limit=1'
    response = requests.get(request_url)
    output = response.json()

    city_name = output['features'][0]['context'][0]['text']

    return city_name
