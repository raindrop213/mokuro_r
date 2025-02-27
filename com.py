from pathlib import Path
import uuid
from loguru import logger
from mokuro import __version__
from mokuro.utils import dump_json, load_json
from natsort import natsorted

# 设置漫画根目录路径
MANGA_ROOT = r"C:\Users\Raindrop\Downloads\[あさぎ龍] 15才"  # 请修改为你的漫画目录路径

def combine_mokuro():
    """将_ocr目录中的JSON文件合并成.mokuro文件"""
    manga_path = Path(MANGA_ROOT)
    if not manga_path.exists():
        logger.error(f"漫画目录不存在: {manga_path}")
        return
        
    ocr_path = manga_path / "_ocr"
    if not ocr_path.exists():
        logger.error(f"OCR目录不存在: {ocr_path}")
        return
        
    # 遍历_ocr下的每个卷目录
    for volume_ocr_path in ocr_path.iterdir():
        if not volume_ocr_path.is_dir():
            continue
            
        volume_name = volume_ocr_path.name
        volume_path = manga_path / volume_name
        
        if not volume_path.exists():
            logger.error(f"卷目录不存在: {volume_path}")
            continue
            
        logger.info(f"处理卷: {volume_name}")
        
        # 获取所有JSON文件路径
        json_paths = natsorted(p.relative_to(volume_ocr_path) for p in volume_ocr_path.glob("*.json"))
        json_paths = {p.with_suffix(""): p for p in json_paths}
        
        # 获取所有图片文件路径
        img_paths = natsorted(
            p.relative_to(volume_path)
            for p in volume_path.glob("*.jpg")  # 假设都是jpg格式
        )
        img_paths = {p.with_suffix(""): p for p in img_paths}
        
        # 创建mokuro文件结构
        out = {
            "version": __version__,
            "title": manga_path.name,
            "title_uuid": str(uuid.uuid4()),  # 生成新的UUID
            "volume": volume_name,
            "volume_uuid": str(uuid.uuid4()),  # 生成新的UUID
            "pages": []
        }
        
        # 合并数据
        for key, json_path_rel in json_paths.items():
            try:
                img_path_rel = img_paths[key]
                # 读取OCR结果
                page_json = load_json(volume_ocr_path / json_path_rel)
                # 添加图片路径
                page_json["img_path"] = str(img_path_rel).replace("\\", "/")
                # 添加到pages数组
                out["pages"].append(page_json)
            except Exception as e:
                logger.error(f"处理文件出错 {json_path_rel}: {e}")
                continue
                
        # 保存mokuro文件
        mokuro_path = manga_path / (volume_name + ".mokuro")
        dump_json(out, mokuro_path)
        logger.info(f"已生成mokuro文件: {mokuro_path}")

if __name__ == "__main__":
    combine_mokuro() 