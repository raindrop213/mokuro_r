from PIL import Image, ExifTags
import os

'''
裁剪成两半，首选

'''

def crop_image(image_path):
    with Image.open(image_path) as img:
        width, height = img.size

        # 只处理宽度大于高度的图片
        if width > height:
            # 计算新的宽度，使其等于高度
            new_width = width // 2

            # 裁剪图片的左半部分
            left_image = img.crop((0, 0, new_width, height))
            left_path = f"{os.path.splitext(image_path)[0]}b{os.path.splitext(image_path)[1]}"
            left_image.save(left_path, quality=95)

            # 裁剪图片的右半部分
            right_image = img.crop((new_width, 0, width, height))
            right_path = f"{os.path.splitext(image_path)[0]}a{os.path.splitext(image_path)[1]}"
            
            right_image.save(right_path, quality=95)
            os.remove(image_path)

            print(f"图片已裁剪：{image_path}")

# 定义处理文件夹内所有图片的函数
def process_images_in_folder(folder_path):
    # 列出文件夹中所有文件
    for filename in os.listdir(folder_path):
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, filename)
        # 检查文件是否为图片
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', 'webp')):
            crop_image(file_path)
        else:
            print(f"跳过非图片文件：{filename}")

# 文件夹路径
folder_path = r'F:\qBit\manga\[押見修造] おかえりアリス\OkaeriArisu v07s\OkaeriArisu_07s'
process_images_in_folder(folder_path)

'''
python sep-all.py
'''