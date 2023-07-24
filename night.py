# This file contains night time images of the village. It also contains the function to convert the day time images to night time images.
# [このファイルには、村の夜間画像が含まれています。昼の画像を夜の画像に変換する機能も含まれています。]

from PIL import Image, ImageEnhance
import numpy as np
import time

# Function to convert the day time images to night time images using brightness factor
# [輝度係数を使って昼間の画像を夜間の画像に変換する機能]
def convert_to_nighttime(input_image_path, output_image_path, brightness_factor=0.5):
    image = Image.open(input_image_path)
    enhancer = ImageEnhance.Brightness(image)
    night_image = enhancer.enhance(brightness_factor)
    night_image.save(output_image_path)

input_path = 'Assets/town.png'
output_path = 'Assets/Background/{}.png'

N = 100

b = np.linspace(0.3,1,N)
for i in range(N):
  convert_to_nighttime(input_path, output_path.format(i), brightness_factor=b[i])
