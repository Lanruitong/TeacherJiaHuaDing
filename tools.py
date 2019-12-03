import os
import shutil
from PIL import Image


# def change_folder_2_char():
#     """将十六进制的文件夹名改为ASCII 字符"""
#     path = '/Users/beiyan/Downloads/by_class/by_class/'
#     for file in os.listdir(path):
#         file_name = os.path.join(path, file)
#         if os.path.isdir(file_name) and len(file) == 2:
#             try:
#                 # 计算出十进制数值
#                 asc_num = int(file[0], 16) * 16 + int(file[1], 16)
#                 # 生成新文件名
#                 new_name = chr(asc_num) + "_" + str(asc_num)
#                 os.renames(file_name, os.path.join(path, new_name))
#             except ValueError:
#                 print(file + " is wrong !")
#

# def generate_train_data():
#     """从图片库中   每个字母挑选前140张图片作为样本(120个训练样本，20个测试样本)"""
#
#     path = 'D:/研一资料/ML/by_class/(a)/hsf_1'
#     train_path = 'D:/MLtrain'
#     test_path = 'D:/MLtest'
#
#     #os.mkdir(train_path)
#     #os.mkdir(test_path)
#
#     for file_name in os.listdir(path):
#
#         # 前120张图片存入训练集 120-140 张图片存入测试集
#         print(file_name)
#         str1 = file_name[-9:-4]
#         index = int(str1)
#         if index < 120:
#             shutil.copyfile(file_name,
#                             os.path.join(train_path, str(index) + ".png"))
#         elif (index >= 120 & index <= 140):
#             shutil.copyfile(file_name,
#                             os.path.join(test_path, str(index) + ".png"))
# generate_train_data()
# image_file_prefix  png图片所在的文件夹
# file_name png      png图片的名字
# txt_path_prefix    转换后txt 文件所在的文件夹
def generate_txt_image(image_file_prefix, file_name, txt_path_prefix):
    """将图片处理成只有0 和 1 的txt 文件"""
    # 将png图片转换成二值图并截取四周多余空白部分
    image_path = os.path.join(image_file_prefix, file_name)
    # convert('L') 将图片转为灰度图 convert('1') 将图片转为二值图
    img = Image.open(image_path, 'r').convert('1').crop((32, 32, 96, 96))

    # 指定转换后的宽 高
    width, height = 32, 32
    img.thumbnail((width, height), Image.ANTIALIAS)

    # 将二值图片转换为0 1，存储到二位数组arr中
    arr = []
    for i in range(width):
        pixels = []
        for j in range(height):
            pixel = int(img.getpixel((j, i)))
            pixel = 0 if pixel == 0 else 1
            pixels.append(pixel)
        arr.append(pixels)

    # 创建txt文件(mac下使用os.mknod()创建文件需要root权限，这里改用复制的方式)
    text_image_file = os.path.join(txt_path_prefix, file_name.split('.')[0] + '.txt')
    empty_txt_path = "D:/empty.txt"
    shutil.copyfile(empty_txt_path, text_image_file)

    # 写入文件
    with open(text_image_file, 'w') as text_file_object:
        for line in arr:
            for e in line:
                text_file_object.write(str(e))
            text_file_object.write("\n")


root_src = 'D:/研一资料/ML/by_class'
root_dst = 'D:/MLtrain'
root_dst2 = 'D:/MLtest'
# 存放训练数据源文件的相对路径
root_src_list = ['(a)/hsf_7', '(b)/hsf_7', '(c)/hsf_7', '(d)/hsf_7', '(e)/hsf_7', '(f)/hsf_7', '(g)/hsf_7',
                 '(h)/hsf_7', '(i)/hsf_7', '(j)/hsf_7', '(k)/hsf_7', '(l)/hsf_7', '(m)/hsf_7', '(n)/hsf_7', '(o)/hsf_7',
                 '(p)/hsf_7', '(q)/hsf_7', '(r)/hsf_7', '(s)/hsf_7', '(t)/hsf_7', '(u)/hsf_7', '(v)/hsf_7', '(w)/hsf_7',
                 '(x)/hsf_7', '(y)/hsf_7', '(z)/hsf_7']
root_dst_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
# 存放测试数据源文件的相对路径
root_src_list2 = ['(a)/hsf_0', '(b)/hsf_0', '(c)/hsf_0', '(d)/hsf_0', '(e)/hsf_0', '(f)/hsf_0', '(g)/hsf_0',
                  '(h)/hsf_0', '(i)/hsf_0', '(j)/hsf_0', '(k)/hsf_0', '(l)/hsf_0', '(m)/hsf_0', '(n)/hsf_0',
                  '(o)/hsf_0', '(p)/hsf_0', '(q)/hsf_0', '(r)/hsf_0', '(s)/hsf_0', '(t)/hsf_0', '(u)/hsf_0',
                  '(v)/hsf_0', '(w)/hsf_0', '(x)/hsf_0', '(y)/hsf_0', '(z)/hsf_0']

# 得到训练样本（a-z一共2600个32*32的txt文件）
for j in range(26):
    i = 0
    for file in os.listdir(os.path.join(root_src, root_src_list2[j])):
        if i < 20:
            generate_txt_image(os.path.join(root_src, root_src_list2[j]), file, os.path.join(root_dst2, root_dst_list[j]))
        else:
            break
        i += 1

# 批量修改文件名使每个训练样本的文件名都含有标签

for j in range(26):
    i = 0
    for file in os.listdir(os.path.join(root_dst2, root_dst_list[j])):
        if i < 20:
            os.rename(os.path.join(root_dst2, root_dst_list[j]) + '/' + file,
                      os.path.join(root_dst2, root_dst_list[j]) + '/' + root_dst_list[j] + '_' + str(i) + '.txt')
        else:
            break
        i += 1

# image_prefix = "/Users/beiyan/Downloads/test/train_data/"
# txt_image_prefix = "/Users/beiyan/Downloads/txt/train_data"
# for file in os.listdir(image_prefix):
#     # 排除 .DS_Store文件
#     if not file.startswith('.'):
#         generate_txt_image(image_prefix, file, txt_image_prefix)
#     print(file)
#
# image_prefix = "/Users/beiyan/Downloads/test/test_data/"
# txt_image_prefix = "/Users/beiyan/Downloads/txt/test_data"
# for file in os.listdir(image_prefix):
#     if not file.startswith('.'):
#         generate_txt_image(image_prefix, file, txt_image_prefix)
#     print(file)

# generate_train_data()
