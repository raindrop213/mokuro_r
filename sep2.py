from PIL import Image, ExifTags
import os

def crop_image(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        print(img.size)

        # 只处理宽度大于高度的图片
        if width > height:
            # 计算新的宽度，使其等于高度
            new_width = width // 2

            directory, filename = os.path.split(image_path)
            # 分割文件名
            file_base, ext = os.path.splitext(filename)
            file_parts = file_base.split('-')
            file_paths0 = os.path.join(directory, file_parts[0] + ext)
            file_paths1 = os.path.join(directory, file_parts[1] + ext)

            # 裁剪图片的左半部分
            left_image = img.crop((0, 0, new_width, height))
            left_path = file_paths1
            left_image.save(left_path, quality=95)

            # 裁剪图片的右半部分
            right_image = img.crop((new_width, 0, width, height))
            right_path = file_paths0
            right_image.save(right_path, quality=95)

            print(f"图片已裁剪为：'{left_path}' 和 '{right_path}'")

def check_image_orientation(image_path):
    with Image.open(image_path) as img:
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation]=='Orientation':
                    break
            exif = dict(img._getexif().items())

            if exif[orientation] == 3:
                rotated = "180 degrees"
            elif exif[orientation] == 6:
                rotated = "270 degrees (clockwise)"
            elif exif[orientation] == 8:
                rotated = "90 degrees (clockwise)"
            else:
                rotated = "not rotated"
        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            rotated = "no EXIF information"

        return rotated

# 定义处理文件夹内所有图片的函数
def process_images_in_folder(folder_path):
    # 列出文件夹中所有文件
    for filename in os.listdir(folder_path):
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, filename)
        # 检查文件是否为图片（这里以.jpg为例）
        if filename.lower().endswith('.jpg'):
            print(f"正在处理图片：{file_path}")
            crop_image(file_path)
            # 可选：调用 check_image_orientation 函数处理每张图片
            # orientation = check_image_orientation(file_path)
            # print(f"{filename} 的方向是：{orientation}")
        else:
            print(f"跳过非图片文件：{filename}")

# 文件夹路径
folder_path = r'H:\qBit\115\【マンガ】\[石黒正数] それでも町は廻っている\[石黒正数] それでも町は廻っている 第01巻'
process_images_in_folder(folder_path)