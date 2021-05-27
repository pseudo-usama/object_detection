"""
This file is used to edit images
Like rotate, resize
"""


from pyperclip import copy
import os
from PIL import Image


def resize(scales_arr, imgs):
    for scale_x, scale_y in scales_arr:
        out_dir = f'{imgs_dir}/{scale_x}x{scale_y}'
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        for img_name, img_extention in imgs:
            img_x, img_y = Image.open(f'{imgs_dir}/{img_name}{img_extention}').size
            final_x, final_y = int(img_x*scale_x), int(img_y*scale_y)

            cmd = f'ffmpeg -i "{imgs_dir}//{img_name}{img_extention}" -vf scale={final_x}:{final_y} "{out_dir}/{img_name}{img_extention}" -y'
            os.system(cmd)

            # print(cmd)
            # copy(cmd)


def rotate(imgs, transpose):
    for img_name, img_extention in imgs:
        out_dir = f'{imgs_dir}/{transpose}'
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        cmd = f'ffmpeg -y -i "{imgs_dir}/{img_name}{img_extention}" -vf "transpose={transpose}" "{out_dir}/{img_name}{img_extention}"'
        os.system(cmd)


imgs_dir = r'full_path_to_imgs_dir'


imgs = [os.path.splitext(img) for img in os.listdir(imgs_dir)
        if os.path.isfile(os.path.join(imgs_dir, img)) and
        (imgs_dir+img).endswith(('.jpg'))]


# rotate(imgs, '1')

resize([
    (0.3, 0.3),
    (0.5, 0.5),
    (2, 2),
], imgs)
