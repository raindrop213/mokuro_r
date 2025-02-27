import os
from pathlib import Path
import subprocess

def process_manga_folders(title_dir):
    # 获取Python解释器路径
    python_exe = "py310-embed/python.exe"
    
    # 确保title_dir是Path对象
    title_path = Path(title_dir)
    
    # 确保路径存在
    if not title_path.exists():
        print(f"错误：目录 {title_path} 不存在")
        return
        
    # 遍历title目录下的所有文件夹
    for manga_dir in title_path.iterdir():
        if manga_dir.is_dir():
            print(f"\n处理漫画：{manga_dir.name}")
            
            try:
                # 构建命令
                cmd = [
                    python_exe,
                    "mokuro",
                    "--disable_confirmation",
                    "--parent_dir",
                    str(manga_dir),
                    "--as_one_file",
                    "False"
                ]
                
                # 执行命令
                subprocess.run(cmd, check=True)
                print(f"成功处理：{manga_dir.name}")
                
            except subprocess.CalledProcessError as e:
                print(f"处理 {manga_dir.name} 时出错：{e}")
            except Exception as e:
                print(f"处理 {manga_dir.name} 时发生未知错误：{e}")

if __name__ == "__main__":
    # 设置title目录路径
    title_directory = r"F:\OneDrive\Website\yuri-hime\title"
    
    print(f"开始处理 {title_directory} 目录下的所有漫画...")
    process_manga_folders(title_directory)
    print("\n所有处理完成！") 