# This file contains fire animation
# [このファイルにはファイヤーアニメーションが含まれています。]
from PIL import Image

# ----------------------Fire Animation----------------------

fire_image = Image.open("Assets\\fire.png")

total_frames = 40
rotation_angle = 0.25
frame_width, frame_height = fire_image.size
output_frames = []

# Rotate the fire image by the rotation angle for each frame [各フレームの回転角度で火災画像を回転させる]
for i in range(total_frames):
    angle = (i - total_frames // 2) * rotation_angle
    rotated_image = fire_image.rotate(angle, resample=Image.BICUBIC, expand=True)
    frame = Image.new("RGBA", (frame_width, frame_height), (0, 0, 0, 0))
    x = (frame_width - rotated_image.width) // 2
    y = frame_height - rotated_image.height 
    frame.paste(rotated_image, (x, y), rotated_image)
    output_frames.append(frame)

# Save the frames as images [フレームを画像として保存する]
for i, frame in enumerate(output_frames):
    frame.save(f"Assets\\Fire\\{i}.png")
