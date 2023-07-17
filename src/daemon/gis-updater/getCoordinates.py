import json
from urllib import request
from urllib import parse 

def get_data(city):

    params = parse.urlencode({
        'city': city,
        'format': 'jsonv2',
    })
    with request.urlopen(f'https://nominatim.openstreetmap.org/search?{params}') as req:
        data = json.loads(req.read().decode())
        return data