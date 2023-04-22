import requests

API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"


def geocode(address):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json",
    }

    response = requests.get(geocoder_request, params=geocoder_params)
    json_response = response.json()
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"]


def get_coordinates(address):
    toponym = geocode(address)
    toponym_coords = toponym["Point"]["pos"]
    long, lat = toponym_coords.split()
    return float(long), float(lat)


def get_ll_spn(address):
    toponym = geocode(address)
    toponym_coords = toponym["Point"]["pos"]
    long, lat = toponym_coords.split()
    ll = ",".join([long, lat])
    envelope = toponym["boundedBy"]["Envelope"]
    l, b = envelope["lowerCorner"].split()
    r, t = envelope["upperCorner"].split()
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0
    span = f"{dx},{dy}"
    return ll, span


def get_map(ll_spn=None, map_type="map", add_params=None):
    if ll_spn:
        map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?l={map_type}"

    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)
    with open("static/img/map.png", "wb") as file:
        file.write(response.content)
