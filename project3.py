#Alan Chen 16976197

import obj_interfaces
import reverse_geolocation
import forward_geolocation
import aqi_api
import get_json_data
import time

def run():
    '''
    UI function that utilizes all of the modules created
    - First takes 5 inputs from user, with no prompting
        - some of the inputs like user_max are spliced to obtain the relevant numbers
    - Those inputs determine what data is relevant
        - I.E:user_range determines the max distance away from the center location
    - Data that is relevant is then printed.
    - In the case that data retrieval is hindered or format of the data
      is not what was expected a error message is printed from the get_json_data
      module and it's exception is caught here to indicate the termination of the
      program.
    - If the program manages to print the output with no problems
      the program ends.
    '''
    user_center = input()
    user_range = input()
    user_threshold = input()
    user_max = input()
    user_aqi = input()
    user_reverse = input()

    user_range = int(user_range[len('RANGE '):])
    user_threshold = int(user_threshold[len('THRESHOLD '):])
    user_max = int(user_max[len('MAX '):])
    
    terminate_program = False

    while terminate_program == False:
        
        try:
            center_coordinates = _determine_forward_method(user_center)

            aqi_and_coordinates = _determine_aqi_method(center_coordinates, user_aqi, user_range, user_threshold, user_max)
            
            locations_names = _determine_reverse_method(user_reverse, aqi_and_coordinates)
            
            _print_output(center_coordinates, aqi_and_coordinates, locations_names)
                
            terminate_program = True
            
        except get_json_data.TerminateProgramError:
            
            terminate_program = True



def _determine_forward_method(center_method: str) -> ('lat', 'lon'):
    '''
    Checks which method to obtain the center coordinates of our location
    returns a tuple of size two that contains latitude and longitude in
    that order.
    - If the keyword NOMINATIM is found in center_method
        - We obtain the data of the center by doing a forward search with
          a ForwardGeoOnline class which takes the location name as
          a parameter and does the forward search to Nominatim for us.
    - If the keyword FILE is found in center_method
        - We obtain the data of the center using a ForwardGeoFile class
          that takes the path indicated as it's parameter.
    '''
    
    if 'NOMINATIM' in center_method:
        center = center_method[len('CENTER NOMINATIM '):]
        if center.strip() != '':
            center_obj = forward_geolocation.ForwardGeoOnline(center)

            return obj_interfaces.get_center_coordinates(center_obj)
    
    if 'FILE' in center_method:
        center_file = center_method[len('CENTER FILE '):]
        if center_file.strip() != '':
            center_obj = forward_geolocation.ForwardGeoFile(center_file)

            return obj_interfaces.get_center_coordinates(center_obj)

    raise get_json_data.TerminateProgramError

    

def _determine_aqi_method(center: ('lat', 'lon'), aqi_method: str, range: int, threshold: int, max: int) -> [['aqi', ('lat', 'lon')]]:

    '''
    Checks which method to use to obtain sensors that satisfy our threshold and range
    This method will return a list with sublists that contain an Aqi value and coordiantes
    which we will use to print out later
    - If the keyword PURPLEAIR is found in aqi_method then we
      would get data from PurpleAir using an AqiOnline class.
    - If the keyword FILE is found in aqi_method we would get the
      data through the file found from the path listed after
      'FILE' instead.
    '''
    
    if 'PURPLEAIR' in aqi_method:
        aqi_obj = aqi_api.AqiOnline()
        
        return obj_interfaces.get_aqi_and_coord_list(aqi_obj, center, range, threshold, max)
    
    if 'FILE' in aqi_method:
        aqi_data_file = aqi_method[len('AQI FILE '):]
        if aqi_data_file.strip() != '':
            aqi_obj = aqi_api.AqiFile(aqi_data_file)
        
            return obj_interfaces.get_aqi_and_coord_list(aqi_obj, center, range, threshold, max)
    

    raise get_json_data.TerminateProgramError

    
def _determine_reverse_method(reverse_method: str, aqi_coord_list: list):
    '''
    Checks which method of reverse search to use: Online or File.
    - If we see the keyword NOMINATIM in the reverse_method string
      we will create a new ReverseGeoOnline class to get data for
      each coordiante in aqi_coord_list, and get its display_name
    - If the keyword is FILE instead, we will get the string of file
      paths and split it by spaces to get the path strings and
      create a new temporary ReverseGeoFile class to fetch the
      display_name from each path in the list
    '''
    if 'NOMINATIM' in reverse_method:
        display_names = []
        for index in range(len(aqi_coord_list)):
            reverse_obj = reverse_geolocation.ReverseGeoOnline(aqi_coord_list[index][1])
            time.sleep(1)
            display_names.append(obj_interfaces.get_display_name(reverse_obj))

        return display_names 
    
    if 'FILES' in reverse_method:
        reverse_files = reverse_method[len('REVERSE FILES '):]
        if reverse_files.strip != '':
            files = reverse_files.split(' ')

            display_names = []
            for file in files:
            
                reverse_obj = reverse_geolocation.ReverseGeoFile(file)
                display_names.append(obj_interfaces.get_display_name(reverse_obj))
            
            return display_names
    
    
    raise get_json_data.TerminateProgramError



def _print_output(center: ('lat', 'lon'), aqi_coord: [['aqi', ('lat', 'lon')]], locations: ['str']) -> None:
    '''
    Function used to print the center coordinate
    location names, coordinates, and the aqi.
    The lists aqi_coord and locations are in the same order order
    '''
    pretty_center_coord = _pretty_coordinates(center)
    print(f'CENTER {pretty_center_coord[0]} {pretty_center_coord[1]}')

    for index in range(len(aqi_coord)):
        aqi = aqi_coord[index][0]
        coordinates = _pretty_coordinates(aqi_coord[index][1])
        location_name = locations[index]
        print(f"AQI {aqi}")
        print(f"{coordinates[0]} {coordinates[1]}")
        print(location_name)
                
    
def _pretty_coordinates(coordinates: ('lat', 'lon')) -> (str):
    '''
    Returns a tuple of size 2 that contains
    the string versions of coordinates lat and lon
    Example:
    - lon: -123.21 -> 123.21/W
    - lon: 123.21 -> 123.21/E
    - lat: 90 -> 90/N
    - lat: -90 -> 90/S
    '''
    lat = coordinates[0]
    lon = coordinates[1]
    if coordinates[0] < 0:
        lat = f"{coordinates[0]*-1}/S"
    if coordinates[0] > 0:
        lat = f"{coordinates[0]}/N"
    if coordinates[1] < 0:
        lon = f"{coordinates[1]*-1}/W"
    if coordinates[1] > 0:
        lon = f"{coordinates[1]}/E"

    return (lat,lon)


    
if __name__ == '__main__':
    run()    







    


