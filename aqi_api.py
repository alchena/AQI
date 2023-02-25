#Alan Chen 16976197

import get_json_data

_PURPLE_AIR_DATA_URL = 'https://www.purpleair.com/data.json'


#
#The 2 classes AqiOnline and AqiFile share an interface
#and both have the same method get_data which returns
#purpleair's aqi sensor data.
#

class AqiOnline():
    def __init__(self):
        self._url = _PURPLE_AIR_DATA_URL
        
    def get_data(self):
        try:
            return get_json_data.download_data(self._url, 'aqi', nominatim_api = False)
        
        except get_json_data.TerminateProgramError:
            raise get_json_data.TerminateProgramError
        
    
class AqiFile():
    def __init__(self, path: str):
        self._path = path
                   
    def get_data(self):
        try:
            
            return get_json_data.get_file_data(self._path, 'aqi')
        
        except get_json_data.TerminateProgramError:
            raise get_json_data.TerminateProgramError



    
        
