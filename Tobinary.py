import os
import shutil
from PIL import Image


def generate_txt_image(image_file_prefix, file_name, txt_path_prefix):
    image_path = os.path.join(image_file_prefix, file_name)
    # convert('1')可将图片转化为二值图
    img = Image.open(image_path, 'r').convert('1').crop((300, 100, 1100, 900))
    width, height = 32,32
    img.thumbnail((width, height), Image.ANTIALIAS)
    arr = []
    for i in range(width):
        pixels = []
        for j in range(height):
            pixel = int(img.getpixel((j, i)))
            pixel = 0 if pixel == 0 else 1
            pixels.append(pixel)
        arr.append(pixels)

    text_image_file = os.path.join(txt_path_prefix, file_name.split('.')[0] + '.txt')
    empty_txt_path = "E:\MLproject\empty.txt"
    shutil.copyfile(empty_txt_path, text_image_file)

    with open(text_image_file, 'w') as text_file_object:
        for line in arr:
            for e in line:
                text_file_object.write(str(e))
            text_file_object.write("\n")


def main():
    generate_txt_image('E:\MLproject', "Z.jpg", "E:\MLproject")


if __name__ == '__main__':
    main()
