import logging
import datetime
from pathlib import Path

DATE = datetime.datetime.now().strftime("%Y-%m-%d")
LOG_DIR = Path(__file__).parent / "logs"
LOG_FILE = LOG_DIR / f"{DATE}.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)

# 设置日志格式
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
)

# 创建日志记录器，记录器名称为'oaldpe-dict-parser'，记录的日志级别为DEBUG
logger = logging.getLogger("oaldpe-dict-parser")
logger.setLevel(logging.DEBUG)

# FileHandler：将日志记录到文件，这里将INFO级别及以上的日志记录到文件
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# StreamHandler：将日志输出到终端，这里将WARNING级别及以上的日志输出到终端
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(formatter)

# 将处理器添加到日志记录器(避免重复添加)
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
