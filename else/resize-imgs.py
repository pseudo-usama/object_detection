"""
This file resize images into different sizes
"""


from pyperclip import copy
import os


imgs_dir, original_x, original_y = r'full_path_images_folder', 4608, 3456
imgs = range(3)


scales_arr = [
    (0.3, 0.3),
    (0.5, 0.5),
    (2, 2),
]

for scale_x, scale_y in scales_arr:
    final_x, final_y = int(original_x*scale_x), int(original_y*scale_y)

    out_dir = f'{imgs_dir}/{scale_x}x{scale_y}'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    for img in imgs:
        img = str(img)
        cmd = f'ffmpeg -i "{imgs_dir}//{img}.jpg" -vf scale={final_x}:{final_y} "{out_dir}/{img}.jpg" -y'
        os.system(cmd)

        # print(cmd)
        # copy(cmd)
