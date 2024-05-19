import os
from PIL import Image    # Pillow                    9.0.0
import pillow_avif       # pillow-avif-plugin        1.2.2
#以上只是其中一个可用版本，并非必须
#必须先安装pip install pillow-avif-plugin才能使用


import os
from PIL import Image
# 不需要特别指明pillow_avif，因为导入Image后pillow_avif会被自动使用

def convert_image_format(folder_path, source_ext, target_ext, target_format):
    """
    将文件夹中所有指定扩展名的图片转换为另一种格式。

    参数:
    - folder_path: 图片所在的文件夹路径
    - source_ext: 源文件扩展名（例如：'avif', 'png', 'jpg'）
    - target_ext: 目标文件扩展名（例如：'png', 'avif', 'jpg'）
    - target_format: 目标图片格式（例如：'PNG', 'AVIF', 'JPEG'）
    """
    for filename in os.listdir(folder_path):
        # 检查文件是否为指定的源格式
        if filename.lower().endswith(f'.{source_ext}'):
            file_path = os.path.join(folder_path, filename)
            try:
                img = Image.open(file_path)
                target_filename = f"{os.path.splitext(file_path)[0]}.{target_ext}"
                img.save(target_filename, target_format)
                os.remove(file_path)
                print(f"{filename} 转换为 {target_ext.upper()} 完成")
            except Exception as e:
                print(f"转换 {filename} 时出错: {e}")

# 示例用法
folder_path = r'F:\qBit\Website\yuri-hime\title\[梶尾真治×鶴田謙二] おもいでエマノン\[梶尾真治×鶴田謙二] Emanon v04 - Emanon Wanderer Part Three'

# AVIF 转 PNG
# convert_image_format(folder_path, 'avif', 'png', 'PNG')
# AVIF 转 JPG
# convert_image_format(folder_path, 'avif', 'jpg', 'JPEG')


# PNG 转 AVIF
# convert_image_format(folder_path, 'png', 'avif', 'AVIF')
# JPG 转 AVIF
convert_image_format(folder_path, 'jpg', 'avif', 'AVIF')
