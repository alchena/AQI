#Alan Chen 16976197

import json
import urllib.request
import urllib.error
from pathlib import Path

_REFERER = 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/alanc15'

class TerminateProgramError(Exception):
    pass
class JsonFormatError(Exception):
    pass

def download_data(url: 'url', api: str, nominatim_api: bool) -> dict:
    '''
    Common function used in the 3 classes of Online api calls
    This function will return the current json data for each api
    depending on what we get back from the call to the url.
    -If any network problems occur an error message is printed.
    -Also checks to see if that data is correctly formated, otherwise
    an error message is printed.
    -A custom error is raised when we get an error so that our
     UI porgram can catch it
    '''
    response = None 
    try:
        if nominatim_api == True:
            request = urllib.request.Request(url, headers = {'Referer' : _REFERER})
        if nominatim_api == False:
            request = urllib.request.Request(url)
            
        response = urllib.request.urlopen(request)
        data = response.read()
        response.close()
        if _check_content_type(response):
            json_text = _get_json_text(data)
            if _check_json_format(json_text, api):
                json_data = json.loads(json_text)
                return json_data
            
    #These are the errors i came across when testing
    #This error is raised if _check_json_format didnt pass
    except JsonFormatError:
        print('FAILED')
        print(f"{response.getcode()} {url}")
        print('FORMAT')
        raise TerminateProgramError
        
    except ValueError:
        print('FAILED')
        print(f"{response.getcode()} {url}")
        print('FORMAT')
        raise TerminateProgramError

    except urllib.error.HTTPError as e:
        print('FAILED')
        print(f"{e.getcode()} {url}")
        print('NOT 200')
        raise TerminateProgramError
    
    except urllib.error.URLError:
        print('FAILED')
        print(f"{url}")
        print('NETWORK')
        raise TerminateProgramError

        
    finally:
        if response != None:
            response.close()


def get_file_data(path: str, format_json: str) -> bool:
    '''
    Common method for the 3 classes that retrieve data
    from a file. Checks to see if the file exists and
    is in the right json format.
    If the file is problematic, doesnt exist,
    or is not in the right format, an error
    message is raised and TerminateProgramError is raised
    so that our UI program can catch it.
    '''
    file = None
        
    try:
        file_path = Path(path)
        file = file_path.open('r')
        data = file.read()
        if _check_json_format(data, format_json):
            return json.loads(data)
        
    #These are the errors i came across when testing    
    except FileNotFoundError:
        print('FAILED')
        print(path)
        print('MISSING')
        raise TerminateProgramError
    except IsADirectoryError:
        print('FAILED')
        print(path)
        print('MISSING')
        raise TerminateProgramError
    except OSError:
        print('FAILED')
        print(path)
        print('MISSING')
        raise TerminateProgramError
    #this error is raised if _check_json_format didnt pass
    except JsonFormatError:
        print('FAILED')
        print(path)
        print('FORMAT')
        raise TerminateProgramError
    
    finally:
        if file != None:
            file.close()

            
def _get_json_text(data: 'bytes') -> str:
    '''
    Used only in download_data to try and decode
    the information given from the url. If the decoding
    is not utf-8 we know that the information is
    incorrect and we raise a custom error
    '''
    try:
        json_text = data.decode(encoding = 'utf-8')
        return json_text
    
    except UnicodeDecodeError:
        raise JsonFormatError


def _check_content_type(response):
    '''
    Checks to see if the Content-Type of the response from
    the url is json, raises a custom error if it isn't
    '''
    if 'application/json' in response.getheader('Content-Type'):
        return True
    else:
        raise JsonFormatError

        
def _check_json_format(data: 'json-dict', format_json: str) -> bool:
    '''
    Function used to see if the dictionary converted from
    json.loads is in the correct format depending on
    which api data we're checking for
    -If any error arrises from checking to see if that key
     exists, a custom error is raised.
    '''
    if format_json == 'aqi':
        
        try:
            
            aqi_data = json.loads(data)
            pm_index = aqi_data['fields'].index('pm')
            age_index = aqi_data['fields'].index('age')
            type_index = aqi_data['fields'].index('Type')
            lat_index = aqi_data['fields'].index('Lat')
            lon_index = aqi_data['fields'].index('Lon')
            sensor_list = aqi_data['data']
            return True
        
        #These are the errors i came across when testing
        except ValueError:
            raise JsonFormatError
        except AttributeError:
            raise JsonFormatError
        except TypeError:
            raise JsonFormatError
        except KeyError:
            raise JsonFormatError

        
    if format_json == 'forward':
        
        try:
            center_data = json.loads(data)
            if len(center_data) == 0:
                raise AttributeError
            lat = float(center_data[0]['lat'])
            lon = float(center_data[0]['lon'])
            return True
        
        #These are the errors i came across when testing    
        except ValueError:
            raise JsonFormatError
        except AttributeError:
            raise JsonFormatError
        except TypeError:
            raise JsonFormatError
        except KeyError:
            raise JsonFormatError


    if format_json == 'reverse':
        
        try:
            reverse_data = json.loads(data)
            if len(reverse_data) == 0:
                raise AttributeError
            display_name = reverse_data['display_name']
            return True

        #These are the errors i came across when testing
        except ValueError:
            raise JsonFormatError
        except AttributeError:
            raise JsonFormatError
        except TypeError:
            raise JsonFormatError
        except KeyError:
            raise JsonFormatError
