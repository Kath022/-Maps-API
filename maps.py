import requests
import sys
from pprint import pprint


def geocode_maps(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print('error')
        sys.exit()

    json_response = response.json()
    # pprint(json_response)
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"].split()

    corner = toponym['boundedBy']['Envelope']
    print(toponym_coodrinates)
    print(corner)

    return toponym_coodrinates


def search_maps(address_ll):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz",
        "results": 10
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        print('error')
        sys.exit()

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # pprint(json_response)

    return json_response


def static_api(coords, scale):
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {
        "ll": ','.join(coords),
        "z": scale,
        "l": "map",
        # "pt": f"{org_point},pm2dgl~{address_ll},home"
    }
    response = requests.get(map_api_server, params=map_params)

    return response.content


