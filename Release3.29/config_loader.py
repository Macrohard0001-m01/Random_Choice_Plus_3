import os
import random
import configparser
import pygame

def get_random_image_from_directory(directory_path):
    """从指定目录中随机选择一个图片文件"""
    if not os.path.exists(directory_path):
        return None
    
    # 支持的图片格式
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tga', '.tiff')
    
    # 获取目录中的所有图片文件
    image_files = [f for f in os.listdir(directory_path) 
                  if f.lower().endswith(image_extensions)]
    
    if not image_files:
        return None
    
    # 随机选择一个图片文件
    selected_image = random.choice(image_files)
    return os.path.join(directory_path, selected_image)

def load_config_to_globals(filepath):
    config = configparser.ConfigParser()
    config.optionxform = str
    
    # 强制使用UTF-8编码读取配置文件
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            config.read_file(f)
    except UnicodeDecodeError:
        # 如果UTF-8失败，尝试GBK（兼容旧文件）
        try:
            with open(filepath, 'r', encoding='gbk') as f:
                config.read_file(f)
        except:
            # 如果都失败，创建默认配置
            print("配置文件编码错误，使用默认配置")
            return
    
    for section in config.sections():
        for key, value in config.items(section):
            var_name = f"{key}"
            try:
                globals()[var_name] = int(value)
            except:
                try:
                    globals()[var_name] = eval(value)
                except:
                    globals()[var_name] = value
