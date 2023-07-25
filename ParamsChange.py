# This file is used to change the parameters in Params.py [このファイルはParams.pyのパラメータを変更するために使用されます。]

import math
import ParamsOld as old
from Params import *

# Alter the following variables to change the size of the window
# [ウィンドウのサイズを変更するには、以下の変数を変更する。]
original_size = (old.WIN_WIDTH,old.WIN_HEIGHT)
new_size = (WIN_WIDTH, WIN_HEIGHT)

def update_coordinate(coord):
    original_x, original_y = original_size
    new_x, new_y = new_size

    # Calculate the scaling factors for x and y coordinates [x座標とy座標のスケーリング係数を計算する。]
    scale_x = new_x / original_x
    scale_y = new_y / original_y

    # Update the coordinates based on the scaling factors [スケーリング係数に基づいて座標を更新]
    updated_x = int(coord[0] * scale_x)
    updated_y = int(coord[1] * scale_y)

    return updated_x, updated_y

def update_radius(radius):
    original_x, original_y = original_size
    new_x, new_y = new_size

    # Calculate the scaling factors for x and y coordinates [x座標とy座標のスケーリング係数を計算する。]
    scale_x = math.sqrt(new_x / original_x)
    scale_y = math.sqrt(new_y / original_y)

    # Update the radius based on the scaling factors [スケーリング係数に基づいて半径を更新する。]
    updated_radius = int(radius * scale_x * scale_y)
    return updated_radius


def update_location_map(location_map):
    updated_location_map = {}
    original_x, original_y = original_size
    new_x, new_y = new_size

    for location, coordinate in location_map.items():
        # Calculate the updated coordinates [更新された座標を計算する]
        updated_x = int(coordinate[0] * new_x / original_x)
        updated_y = int(coordinate[1] * new_y / original_y)

        # Add the updated coordinates to the updated location map [更新された座標を更新されたロケーションマップに追加する]
        updated_location_map[location] = (updated_x, updated_y)

    # Convert the updated location map to a string representation [更新されたロケーションマップを文字列表現に変換する。]
    map_string = str(updated_location_map)

    return map_string

############################################################

# Coordinate Change [座標変更]

print("EMOJI_SIZE =",update_coordinate(old.EMOJI_SIZE))
print("FIRE_SIZE =",update_coordinate(old.FIRE_SIZE))
print("FIRE_CENTER =",update_coordinate(old.FIRE_CENTER))
print("TavernCenter =",update_coordinate(old.TavernCenter))
print("Character_Size =",update_coordinate(old.Character_Size))


############################################################

# Radius Change [半径の変更]

print("TavernRadius =",update_radius(old.TavernRadius))


##################################################################################

# LOCATION_MAP change [LOCATION_MAPの変更]

print("LOCATION_MAP =",update_location_map(old.LOCATION_MAP))






