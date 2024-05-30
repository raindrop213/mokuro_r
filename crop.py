from PIL import Image
import os

def crop_image(input_path, output_path, crop_edges):
    """
    根据指定的上下左右裁剪边缘裁剪图片。

    :param input_path: 输入图片的路径。
    :param output_path: 输出图片的路径。
    :param crop_edges: 要裁剪的边缘大小，格式为(left, top, right, bottom)。
    """
    # 打开图片
    with Image.open(input_path) as img:
        # 获取图片的尺寸
        img_width, img_height = img.size
        
        # 获取裁剪边缘
        left, top, right, bottom = crop_edges
        
        # 计算裁剪区域
        crop_left = left
        crop_top = top
        crop_right = img_width - right
        crop_bottom = img_height - bottom
        
        # 裁剪图片
        img_cropped = img.crop((crop_left, crop_top, crop_right, crop_bottom))
        
        # 保存裁剪后的图片
        img_cropped.save(output_path, quality=95)

def batch_crop_images(folder_path, output_folder, crop_edges):
    """
    批量裁剪文件夹内的所有图片，并允许偏移。

    :param folder_path: 包含图片的文件夹路径。
    :param output_folder: 裁剪后图片的输出文件夹路径。
    :param crop_edges: 要裁剪的边缘大小，格式为(left, top, right, bottom)。
    """
    # 遍历文件夹内的所有文件
    for filename in os.listdir(folder_path):
        # 构造输入和输出的完整路径
        input_path = os.path.join(folder_path, filename)
        output_path = os.path.join(output_folder, filename)
        
        # 检查文件是否为图片
        if input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            print(f'Processing {filename}...')
            crop_image(input_path, output_path, crop_edges)
            print(f'{filename} has been processed and saved to {output_path}.')

# 设置你的文件夹路径
name = "F:\qBit\manga\[びみ太] 田舎に帰るとやけになついた褐色ポニテショタがいる\[びみ太] 田舎に帰るとやけになついた褐色ポニテショタがいる 第03巻"
folder_path = name  # 你的输入文件夹路径
output_folder = name+"sep"  # 你的输出文件夹路径

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 批量裁剪图片，可以指定上下左右裁剪边缘大小
# crop_edges格式为(left, top, right, bottom)
batch_crop_images(folder_path, output_folder, crop_edges=(201, 0, 201, 0))  # 向左裁剪10像素，向上裁剪20像素，向右裁剪10像素，向下裁剪20像素
