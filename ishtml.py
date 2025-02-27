
import os

# 漫画主目录
root_dir = r'F:\website\yuri-hime\title'  # 替换为你的实际路径

# 遍历每部漫画文件夹
for manga in os.listdir(root_dir):
    manga_path = os.path.join(root_dir, manga)
    if os.path.isdir(manga_path):
        # 遍历每卷图片文件夹
        for volume in os.listdir(manga_path):
            volume_path = os.path.join(manga_path, volume)
            if os.path.isdir(volume_path) and not volume.startswith('_ocr'):
                # 生成应有的 HTML 文件名
                html_file = f"{volume}.html"
                html_path = os.path.join(manga_path, html_file)

                # 检查 HTML 文件是否存在
                if not os.path.isfile(html_path):
                    print(f"缺少 HTML 文件: {html_path}")
