import math
from Params import *

def update_coordinate(coord, original_size, new_size):
    original_x, original_y = original_size
    new_x, new_y = new_size

    # Calculate the scaling factors for x and y coordinates
    scale_x = new_x / original_x
    scale_y = new_y / original_y

    # Update the coordinates based on the scaling factors
    updated_x = int(coord[0] * scale_x)
    updated_y = int(coord[1] * scale_y)

    return updated_x, updated_y

def update_radius(radius, original_size, new_size):
    original_x, original_y = original_size
    new_x, new_y = new_size

    # Calculate the scaling factors for x and y coordinates
    scale_x = math.sqrt(new_x / original_x)
    scale_y = math.sqrt(new_y / original_y)

    # Update the radius based on the scaling factors
    updated_radius = int(radius * scale_x * scale_y)

    return updated_radius



#####Coordinate change

original_coord = (100, 200)
original_window_size = (1150, 800)
new_window_size = (2000, 1500)

updated_coord = update_coordinate(original_coord, original_window_size, new_window_size)
print(updated_coord)  # Output: (128, 256)


############################################################

#Radius (1 variable change)
original_radius = 100
original_window_size = (1150, 800)
new_window_size = (2000, 1500)

updated_radius = update_radius(original_radius, original_window_size, new_window_size)
print(updated_radius)  # Output: 63



##################################################################################

# LOCATION_MAP change

def update_location_map(location_map, original_size, new_size):
    updated_location_map = {}
    original_x, original_y = original_size
    new_x, new_y = new_size

    for location, coordinate in location_map.items():
        # Calculate the updated coordinates
        updated_x = int(coordinate[0] * new_x / original_x)
        updated_y = int(coordinate[1] * new_y / original_y)

        # Add the updated coordinates to the updated location map
        updated_location_map[location] = (updated_x, updated_y)

    # Convert the updated location map to a string representation
    map_string = str(updated_location_map)

    return map_string



original_window_size = (800, 600)
new_window_size = (1024, 768)

updated_map_string = update_location_map(LOCATION_MAP, original_window_size, new_window_size)
print(updated_map_string)







