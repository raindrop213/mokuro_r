from PIL import Image
import os

def crop_image_to_center(input_path, output_path, size):
    """
    裁剪图片为指定大小并居中。

    :param input_path: 输入图片的路径。
    :param output_path: 输出图片的路径。
    :param size: 裁剪后的大小，格式为(width, height)。
    """
    # 打开图片
    with Image.open(input_path) as img:
        # 获取图片的尺寸
        img_width, img_height = img.size
        print()
        
        # 计算裁剪区域
        new_width, new_height = size
        left = (img_width - new_width) / 2
        top = (img_height - new_height) / 2
        right = (img_width + new_width) / 2
        bottom = (img_height + new_height) / 2
        
        # 裁剪图片
        img_cropped = img.crop((left, top, right, bottom))
        
        # 保存裁剪后的图片
        img_cropped.save(output_path, quality=95)

def batch_crop_images(folder_path, output_folder, size):
    """
    批量裁剪文件夹内的所有图片。

    :param folder_path: 包含图片的文件夹路径。
    :param output_folder: 裁剪后图片的输出文件夹路径。
    :param size: 裁剪后的大小，格式为(width, height)。
    """
    # 遍历文件夹内的所有文件
    for filename in os.listdir(folder_path):
        # 构造输入和输出的完整路径
        input_path = os.path.join(folder_path, filename)
        output_path = os.path.join(output_folder, filename)
        
        # 检查文件是否为图片
        if input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            print(f'Processing {filename}...')
            crop_image_to_center(input_path, output_path, size)
            print(f'{filename} has been processed and saved to {output_path}.')

# 设置你的文件夹路径
folder_path = r'C:\Users\Raindrop\Downloads\FireShot\新建文件夹'  # 你的输入文件夹路径
output_folder = r'C:\Users\Raindrop\Downloads\FireShot\新建文件夹'  # 你的输出文件夹路径

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 批量裁剪图片
batch_crop_images(folder_path, output_folder, size=(2030, 1440))
# batch_crop_images(folder_path, output_folder, size=(1015, 1440))
# batch_crop_images(folder_path, output_folder, size=(1356,2038))