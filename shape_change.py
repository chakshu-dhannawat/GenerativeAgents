import math

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








