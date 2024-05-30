from PIL import Image, ExifTags
import os

def crop_and_split_image(input_path, output_folder, crop_edges):
    """
    根据指定的上下左右裁剪边缘裁剪图片，并将图片裁剪成两半。
    
    :param input_path: 输入图片的路径。
    :param output_folder: 输出图片的文件夹路径。
    :param crop_edges: 要裁剪的边缘大小，格式为(left, top, right, bottom)。
    """
    with Image.open(input_path) as img:
        img_width, img_height = img.size

        # 获取裁剪边缘
        left, top, right, bottom = crop_edges

        # 计算裁剪区域
        crop_left = left
        crop_top = top
        crop_right = img_width - right
        crop_bottom = img_height - bottom

        # 裁剪图片边缘
        img_cropped = img.crop((crop_left, crop_top, crop_right, crop_bottom))

        # 获取裁剪后的图片尺寸
        cropped_width, cropped_height = img_cropped.size

        # 只处理宽度大于高度的图片
        if cropped_width > cropped_height:
            # 计算新的宽度，使其等于高度的一半
            new_width = cropped_width // 2

            # 裁剪图片的左半部分
            left_image = img_cropped.crop((0, 0, new_width, cropped_height))
            left_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_path))[0]}_left{os.path.splitext(input_path)[1]}")
            left_image.save(left_path, quality=95)

            # 裁剪图片的右半部分
            right_image = img_cropped.crop((new_width, 0, cropped_width, cropped_height))
            right_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_path))[0]}_right{os.path.splitext(input_path)[1]}")
            right_image.save(right_path, quality=95)

            print(f"图片已裁剪并分成两半：{input_path}")
        else:
            output_path = os.path.join(output_folder, os.path.basename(input_path))
            img_cropped.save(output_path, quality=95)
            print(f"图片已裁剪：{input_path}")

def batch_crop_and_split_images(folder_path, output_folder, crop_edges):
    """
    批量裁剪和分割文件夹内的所有图片。

    :param folder_path: 包含图片的文件夹路径。
    :param output_folder: 裁剪后图片的输出文件夹路径。
    :param crop_edges: 要裁剪的边缘大小，格式为(left, top, right, bottom)。
    """
    for filename in os.listdir(folder_path):
        input_path = os.path.join(folder_path, filename)
        if input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            crop_and_split_image(input_path, output_folder, crop_edges)
        else:
            print(f"跳过非图片文件：{filename}")

# 设置文件夹路径
input_folder = r'F:\qBit\manga\[NON] adabana―徒花―\adabana v03 DL'
output_folder = input_folder + "sep"
os.makedirs(output_folder, exist_ok=True)

# 批量裁剪和分割图片 (left, top, right, bottom)。
crop_edges = (210, 0, 210, 0)
batch_crop_and_split_images(input_folder, output_folder, crop_edges)
