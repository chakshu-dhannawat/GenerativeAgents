from PIL import Image
import numpy as np
from skimage.transform import warp, AffineTransform

fire_image = Image.open("Assets\\fire.png")

total_frames = 40
rotation_angle = 1
frame_width, frame_height = fire_image.size
output_frames = []

# Generate mesh grid for warping
grid_x, grid_y = np.meshgrid(np.arange(frame_width), np.arange(frame_height))
mesh_grid = np.stack((grid_x, grid_y), axis=-1)

for i in range(total_frames):
    angle = (i - total_frames // 2) * rotation_angle
    rotated_image = fire_image.rotate(angle, resample=Image.BICUBIC, expand=True)
    rotated_image_array = np.array(rotated_image)

    # Apply warping to the image
    warping_factor = 0.1  # Adjust this value to control the intensity of warping
    random_displacements = np.random.normal(0, warping_factor, mesh_grid.shape)
    warped_mesh_grid = mesh_grid + random_displacements

    # Create an affine transformation matrix
    transform = AffineTransform(scale=(1, 1), rotation=0, translation=(0, 0))
    transform.params[0:2, 2] = np.mean(random_displacements, axis=(0, 1))

    # Warp the image using the affine transformation
    warped_image_array = warp(rotated_image_array, transform.inverse, output_shape=(frame_height, frame_width))

    # Create a new image from the warped image array
    warped_image = Image.fromarray((warped_image_array * 255).astype(np.uint8))

    frame = Image.new("RGBA", (frame_width, frame_height), (0, 0, 0, 0))
    x = (frame_width - warped_image.width) // 2
    y = (frame_height - warped_image.height) // 2
    frame.paste(warped_image, (x, y), warped_image)
    output_frames.append(frame)

for i, frame in enumerate(output_frames):
    frame.save(f"Assets\\Fire\\{i}.png")
