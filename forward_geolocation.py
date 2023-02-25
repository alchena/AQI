#Alan Chen 16976197

import urllib.parse
import get_json_data

_NOMINATIM_SEARCH_URL = 'https://nominatim.openstreetmap.org/search?'


#The 2 classes ForwardGeoOnline and ForwardGeoFile
#share an interface and both contain the method called
#get_location_data which returns a list containing
#dictionaries from a call to Nominatims search api

class ForwardGeoOnline():
    
    def __init__(self, user_center: str):
        self._url = self._build_search_url(user_center)

    def get_location_data(self) -> [dict]:
        try:
            return get_json_data.download_data(self._url, 'forward', nominatim_api = True)
        
        except get_json_data.TerminateProgramError:
            raise get_json_data.TerminateProgramError

    def _build_search_url(self, user_location):
        query_parameters = [
        ('q', user_location),
        ('format', 'json')
        ]
        return _NOMINATIM_SEARCH_URL + urllib.parse.urlencode(query_parameters)



class ForwardGeoFile():
    def __init__(self, path: str):
        self._center_file = path        
        

    def get_location_data(self) -> [dict]:
        try:
            return get_json_data.get_file_data(self._center_file, 'forward')
        
        except get_json_data.TerminateProgramError:
            raise get_json_data.TerminateProgramError




