#Alan Chen 16976197

import get_json_data
import urllib.parse
import time

_NOMINATIM_REVERSE_URL = 'https://nominatim.openstreetmap.org/reverse?'

#The 2 Classes ReverseGeoOnline and ReverseFile share an interface
#both classes contain the get_name_data method that returns
#a dictionary that contains information for a reverse search using
#Nominatims reverse search api

class ReverseGeoOnline():

    def __init__(self, coordinates: ('lat', 'lon')):
        self._lat = float(coordinates[0])
        self._lon = float(coordinates[1])
        
    def get_name_data(self):
        url = self._build_search_url(self._lat, self._lon)
        try:
            return get_json_data.download_data(url, 'reverse', nominatim_api = True)
        
        except get_json_data.TerminateProgramError:
            raise get_json_data.TerminateProgramError


    def _build_search_url(self, lat: float, lon: float):
        query_parameters = [
        ('lat', lat),
        ('lon', lon),
        ('format', 'json')
        ]
        return _NOMINATIM_REVERSE_URL + urllib.parse.urlencode(query_parameters)
    

class ReverseGeoFile():

    def __init__(self, path: str):
        self._path = path

    def get_name_data(self):
        try:

            return get_json_data.get_file_data(self._path, 'reverse')
        
        except get_json_data.TerminateProgramError:
            raise get_json_data.TerminateProgramError
