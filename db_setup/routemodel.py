# from db_setup.init import connect_to_db
import numpy as np # Import for numpy array
import gpxpy # Import to allow easier parsing of gpx file
import math

def gpx_parser(output_file="output.txt"):
    """
    Convert gpx files into an array with
    
    - stage name
    - lat
    - long
    - elevation (m)
    - distance (km)
    - orientation (deg)

    As the respective columns.
    """
    
    # Declare lists to hold data
    data = []
    stage_names = []
    lats = []
    lons = []
    elevations = []

    # Open gpx file and utilize gpxpy to parse the file
    with open("gpx_asc24/0_FullBaseRoute.gpx", "r") as gpx_file:
        # gpxpy stores the data in a much easier readable format
        gpx = gpxpy.parse(gpx_file)

    # Iterate through all track segments and points
    for track in gpx.tracks:
        for segment in track.segments:
            for points in segment.points:
                stage_names.append(track.name)
                lats.append(points.latitude)
                lons.append(points.longitude)
                elevations.append(points.elevation)
    
    # Stores distance and orientation from returned data
    distance = distance_calc()
    orientation = orientation_calc(lats, lons)
    
    # Convert lists to numpy arrays
    np_stage_names = np.array(stage_names)
    np_lats = np.array(lats)
    np_lons = np.array(lons)
    np_elevations = np.array(elevations)
    np_distance = np.array(distance) # Assuming returend data was list
    np_orientation = np.array(orientation) # Assuming returend data was list
    
    # Zip the individual arrays together 
    # Specify a structured dtype (data type) for each column
    # Need to add distance and orientation after
    data = np.array(list(zip(np_stage_names, np_lats, np_lons, np_elevations)), dtype=[
            ('stage_name', 'U50'), 
            ('lat', 'f8'), 
            ('lon', 'f8'), 
            ('ele', 'f8') 
        ])

    # To test
    np.savetxt(output_file, data, fmt="%s,%.8f,%.8f,%.2f", header="Stage Name, Latitude, Longitude, Elevation", delimiter=',', comments='')
    
    return data


def distance_calc():
    """
    Calculate cumulative distances of a stage at each point.
    """
    distances = []
    return distances


def orientation_calc(lats, lons):
    """
    Calculate the orientations of the car (bearing) with True North being 0 degrees.
    Using this formula for bearing: 
    https://www.movable-type.co.uk/scripts/latlong.html#:~:text=a%20constant%20bearing!-,Bearing,-In%20general%2C%20your
    """
    orientations = []
    for i in range(len(lats)-1):
        lat1 = lats[i]
        lon1 = lons[i]
        lat2 = lats[i+1]
        lon2 = lons[i+1]
        
        # math functions need values in radians
        rad_x1 = math.radians(lon1)
        rad_x2 = math.radians(lon2)
        rad_y1 = math.radians(lat1)
        rad_y2 = math.radians(lat2)
        diff_lon = rad_x2 - rad_x1
        
        # using spherical geometry for this formula
        distance_y = math.sin(diff_lon) * math.cos(rad_y2)
        distance_x = math.cos(rad_y1) * math.sin(rad_y2) - \
            math.sin(rad_y1) * math.cos(rad_y2) * math.cos(diff_lon)
        angle = math.atan2(distance_y, distance_x)
        # convert angle to bearing in degrees
        bearing = (angle*180/math.pi + 360) % 360
        
        orientations.append(bearing)
    return orientations


def init_table():
    """
    Create table for route-model in postgres database.
    """
    return None


def insert_data():
    """
    Insert data into routmodel table in postgres database
    """
    return None

gpx_parser("gpx_output.txt")