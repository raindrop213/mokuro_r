from PIL import Image
import os

def crop_image_to_center(image, size):
    """
    裁剪图片为指定大小并居中。

    :param image: 输入图片对象。
    :param size: 裁剪后的大小，格式为(width, height)。
    :return: 裁剪后的图片对象。
    """
    img_width, img_height = image.size
    
    # 计算裁剪区域
    new_width, new_height = size
    left = (img_width - new_width) / 2
    top = (img_height - new_height) / 2
    right = (img_width + new_width) / 2
    bottom = (img_height + new_height) / 2
    
    # 裁剪图片
    img_cropped = image.crop((left, top, right, bottom))
    return img_cropped

def crop_image_halves(image):
    """
    将图片裁剪成左右两半。

    :param image: 输入图片对象。
    :return: 左右两半的图片对象（left_image, right_image）。
    """
    width, height = image.size

    # 只处理宽度大于高度的图片
    if width > height:
        new_width = width // 2

        # 裁剪图片的左半部分
        left_image = image.crop((0, 0, new_width, height))
        
        # 裁剪图片的右半部分
        right_image = image.crop((new_width, 0, width, height))
        
        return left_image, right_image
    return None, None

def process_and_save_image(input_path, output_folder, size):
    """
    处理单张图片，并裁剪成指定大小和两半后保存。

    :param input_path: 输入图片的路径。
    :param output_folder: 输出文件夹路径。
    :param size: 裁剪后的大小，格式为(width, height)。
    """
    with Image.open(input_path) as img:
        # 先裁剪居中
        img_cropped_center = crop_image_to_center(img, size)
        
        # 再裁剪成左右两半
        left_image, right_image = crop_image_halves(img_cropped_center)
        
        # 构造输出路径
        base_name = os.path.basename(input_path)
        name, ext = os.path.splitext(base_name)
        
        if left_image and right_image:
            left_path = os.path.join(output_folder, f"{name}b{ext}")
            right_path = os.path.join(output_folder, f"{name}a{ext}")
            
            left_image.save(left_path, quality=95)
            right_image.save(right_path, quality=95)
            print(f"{base_name} has been processed and saved to {output_folder}.")
        else:
            print(f"Skipped non-landscape image: {base_name}")

def batch_process_images(folder_path, output_folder, size):
    """
    批量处理文件夹内的所有图片。

    :param folder_path: 包含图片的文件夹路径。
    :param output_folder: 裁剪后图片的输出文件夹路径。
    :param size: 裁剪后的大小，格式为(width, height)。
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历文件夹内的所有文件
    for filename in os.listdir(folder_path):
        # 构造输入的完整路径
        input_path = os.path.join(folder_path, filename)
        
        # 检查文件是否为图片
        if input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            print(f'Processing {filename}...')
            process_and_save_image(input_path, output_folder, size)
        else:
            print(f'Skipped non-image file: {filename}')

# 设置你的文件夹路径
folder_path = r'C:\Users\Raindrop\Downloads\FireShot\新建文件夹'  # 你的输入文件夹路径
output_folder = r'C:\Users\Raindrop\Downloads\FireShot4'  # 你的输出文件夹路径

# 批量处理图片
batch_process_images(folder_path, output_folder, size=(2030, 1440))
