# This file is used to change the parameters in Params.py

import math
import ParamsOld as old
from Params import *

# Alter the following variables to change the size of the window
original_size = (old.WIN_WIDTH,old.WIN_HEIGHT)
new_size = (WIN_WIDTH, WIN_HEIGHT)

def update_coordinate(coord):
    original_x, original_y = original_size
    new_x, new_y = new_size

    # Calculate the scaling factors for x and y coordinates
    scale_x = new_x / original_x
    scale_y = new_y / original_y

    # Update the coordinates based on the scaling factors
    updated_x = int(coord[0] * scale_x)
    updated_y = int(coord[1] * scale_y)

    return updated_x, updated_y

def update_radius(radius):
    original_x, original_y = original_size
    new_x, new_y = new_size

    # Calculate the scaling factors for x and y coordinates
    scale_x = math.sqrt(new_x / original_x)
    scale_y = math.sqrt(new_y / original_y)

    # Update the radius based on the scaling factors
    updated_radius = int(radius * scale_x * scale_y)
    # print(updated_radius)
    return updated_radius


def update_location_map(location_map):
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

############################################################

# Coordinate Change

print("EMOJI_SIZE =",update_coordinate(old.EMOJI_SIZE))
print("FIRE_SIZE =",update_coordinate(old.FIRE_SIZE))
print("FIRE_CENTER =",update_coordinate(old.FIRE_CENTER))
print("TavernCenter =",update_coordinate(old.TavernCenter))
print("Character_Size =",update_coordinate(old.Character_Size))


############################################################

# Radius Change

print("TavernRadius =",update_radius(old.TavernRadius))


##################################################################################

# LOCATION_MAP change

print("LOCATION_MAP =",update_location_map(old.LOCATION_MAP))






