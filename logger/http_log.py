import logging
from logging import handlers
from setting import PROJECT_ROOT_PATH
import os

# 定义 logger 对象来记录日志
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

# 设置logging 格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 定义单个文件输出日志 处理器
# lf_handler = logging.FileHandler(os.path.join(PROJECT_ROOT_PATH, "logger","print.log"),
#                                  mode='a', encoding='UTF-8')
# 定义多个文件输出日志 处理器
lf_rotate_handler = handlers.RotatingFileHandler(os.path.join(PROJECT_ROOT_PATH, "logger", "print.log"),
                                                 mode='w', maxBytes=10 * 1024 * 1024, backupCount=5, encoding='UTF-8')
lf_rotate_handler.setLevel(logging.INFO)  # 等级设置
lf_rotate_handler.setFormatter(formatter)  # 格式设置

# 定义console输出日志 处理器
lc_handler = logging.StreamHandler()
lc_handler.setLevel(logging.INFO)
lc_handler.setFormatter(formatter)

# 绑定
logger.addHandler(lf_rotate_handler)
# logger.addHandler(lc_handler)
