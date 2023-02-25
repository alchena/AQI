#Alan Chen 16976197

import math
#The functions in this file take advantage of the class interfaces
def get_aqi_and_coord_list(AqiObj, center: ('lat', 'lon'), range_miles: int, threshold: int, num_results: int):
    '''
    Takes in a AqiObj(can be AqiOnline or AqiFile) and returns
    a list with sublist, that contains an aqi value of the senosr
    as the first element and a tuple that contains
    the latitude and longitude of the sensor as the second element.
    
    - The conditions that let a sensor be appended into the list are:
        - if the sensor is within range_miles of the center
        - if the sensor is outside
        - if the sensor last reported less than an hour ago
        - if the sensor is at or exceeds the threshold AQI
        
    - The size of the list is equal to num_results if there are greater
      than num_results of sensors that satisfies the conditions
    - The size of the list is less than num_results if there are less
      than num_results of sensors that satisfies the conditions
    '''
    data = AqiObj.get_data()
    #Got all the indexes for the things that needed checking
    pm_index = data['fields'].index('pm')
    age_index = data['fields'].index('age')
    type_index = data['fields'].index('Type')
    lat_index = data['fields'].index('Lat')
    lon_index = data['fields'].index('Lon')
    #Got the entire list of just the sensors
    sensor_list = data['data']

    aqi_with_coordinates = []

    #Looping through the list of sensors and checking for conditions
    for sensor in sensor_list:
        
        sensor_lat_lon = (sensor[lat_index], sensor[lon_index])
        
        if _sensor_within_dist(center, sensor_lat_lon, range_miles):
            if sensor[type_index] == 0:
                if sensor[age_index] != None and sensor[age_index] <= 3600:
                    if sensor[pm_index] != None:
                        aqi = _get_aqi(sensor[pm_index])
                        if aqi >= threshold:
                            aqi_with_coordinates.append([aqi, sensor_lat_lon])
                        
    
    if len(aqi_with_coordinates) <= num_results:
        return sorted(aqi_with_coordinates, reverse = True)
    else:
        return sorted(aqi_with_coordinates, reverse = True)[:num_results] 


def get_center_coordinates(ForwardObj):
    '''
    Takes in a ForwardObj(which can be ForwardGeoOnline or ForwardGeoFile)
    and gets the coordinates from the data.
    '''
    
    address_dict = ForwardObj.get_location_data()
    #Converted data from string to a float
    lat = float(address_dict[0]['lat'])
    lon = float(address_dict[0]['lon'])
    return (lat,lon)
    
        
def get_display_name(ReverseObj):
    '''
    Takes in a ReverseObj(which can be either ReverseGeoOnline
    or ReverseGeoFile) and returns the display_name of the location
    '''
    address_dict = ReverseObj.get_name_data()
    display_name = address_dict['display_name']
    return display_name



def _sensor_within_dist(center: ('lat', 'lon'), location: ('lat', 'lon'), miles_range: int):
    '''
    Function used in get_aqi_and_coord_list to determine
    if distance is within miles_range. The equirectangular distance
    formula is used here
    '''
    if location[0] == None or location[1] == None:
        return False
    
    lat_locat = location[0]
    lon_locat = location[1]

    lat_cent = center[0]
    lon_cent = center[1]
    radius = 3958.8
    
    dlat = (lat_locat - lat_cent) * (math.pi/180)
    dlon = (lon_locat - lon_cent) * (math.pi/180)

    #checks to see if the 2 longitudes are <-360, and >360
    #if it is we subtract 360 to get the shortest
    #distance between the 2.
    if dlon > math.pi:
        dlon = (2*math.pi) - dlon
    if dlon < -math.pi:
        dlon = (2*math.pi) - dlon*-1
        
    alat = (lat_cent + lat_locat)/2 * (math.pi/180)
    x = dlon * math.cos(alat)
    
    distance = math.sqrt(x**2 + dlat**2) * radius
    if distance <= miles_range:
        return True
    else:
        return False
    

    
def _get_aqi(pm: float) -> int:
    '''
    Table used to determine what aqi value is depending
    on the pm concentration, returns its associated AQI
    value.
    '''
    if 0.0 <= pm < 12.1:
       aqi =  50/12 * pm
       return round(aqi + 0.00001)
    if 12.1 <= pm < 35.5:
        slope = 49/23.3
        y_intercept = 51 - (slope * 12.1)
        aqi = round(slope * pm + (y_intercept) + 0.00001)
        return aqi
    if 35.5 <= pm < 55.5:
        slope = 49/19.9
        y_intercept = 101 - (slope * 35.5)
        aqi = round(slope * pm + (y_intercept) + 0.00001)
        return aqi
    if 55.5 <= pm < 150.5:
        slope = 49/94.9
        y_intercept = 151 - (slope * 55.5)
        aqi = round(slope * pm + (y_intercept) + 0.00001)
        return aqi 
    if 150.5 <= pm < 250.5:
        slope = 99/99.9
        y_intercept = 201 - (slope*150.5)
        aqi = round(slope * pm + (y_intercept) + 0.00001)
        return aqi
    if 250.5 <= pm < 350.5:
        slope = 99/99.9
        y_intercept = 301 - (slope * 250.5)
        aqi = round(slope * pm + (y_intercept) + 0.00001)
        return aqi
    if 350.5 <= pm < 500.5:
        slope = 99/149.9
        y_intercept = 401 - (slope * 350.5)
        aqi = round(slope * pm + (y_intercept) + 0.00001)
        return aqi
    if pm >= 500.5:
        return 501

#test for aqi
assert _get_aqi(0.0) == 0
assert _get_aqi(5.9) == 25
assert _get_aqi(12.1) == 51
assert _get_aqi(32.8) == 95
assert _get_aqi(35.5) == 101 
assert _get_aqi(52) == 142
assert _get_aqi(55.5) == 151
assert _get_aqi(80.99) == 164
assert _get_aqi(150.5) == 201
assert _get_aqi(240.190321) == 290
assert _get_aqi(250.5) == 301
assert _get_aqi(320.19) == 370
assert _get_aqi(350.5) == 401 
assert _get_aqi(499.999) == 500
assert _get_aqi(500.5) == 501
assert _get_aqi(600) == 501
