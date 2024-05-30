import os
from PIL import Image

def swap_images_in_pairs(input_folder, output_folder):
    # 创建输出文件夹如果它不存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取所有jpg文件并排序
    files = sorted([f for f in os.listdir(input_folder) if f.endswith('.jpg')])

    # 处理成对的图片
    for i in range(0, len(files), 2):
        if i + 1 < len(files):
            # 获取图片路径
            img1_path = os.path.join(input_folder, files[i])
            img2_path = os.path.join(input_folder, files[i + 1])

            # 打开图片
            img1 = Image.open(img1_path)
            img2 = Image.open(img2_path)

            # 保存图片到输出文件夹，交换顺序
            img1.save(os.path.join(output_folder, files[i + 1]))
            img2.save(os.path.join(output_folder, files[i]))
        else:
            # 如果总数是奇数，最后一张图片不交换，直接复制
            img_path = os.path.join(input_folder, files[i])
            img = Image.open(img_path)
            img.save(os.path.join(output_folder, files[i]))

# 示例使用方法
input_folder = r'H:\website\yuri-hime\title\[NON] adabana―徒花―\[NON] adabana―徒花― 第03巻'
output_folder = r'H:\website\yuri-hime\title\[NON] adabana―徒花―\[NON] adabana―徒花― 第03巻2'
swap_images_in_pairs(input_folder, output_folder)
