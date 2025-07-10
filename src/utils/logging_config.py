# src/utils/logging_config.py
import logging
import logging.handlers
from pathlib import Path
import os
import shutil

# 标志位防止重复初始化
_initialized = False

def setup_logging():
    """安全的日志配置（每次运行创建新文件，保留最多5个历史日志）"""
    global _initialized
    if _initialized:
        return
    _initialized = True

    PROJECT_ROOT = Path(__file__).parent.parent
    LOG_DIR = PROJECT_ROOT / "logs"
    LOG_DIR.mkdir(exist_ok=True)

    # 清理并轮转旧日志（确保最多保留5个）
    def rotate_logs():
        log_files = sorted(LOG_DIR.glob("game*.log"), key=os.path.getmtime, reverse=True)
        for i, old_log in enumerate(log_files[4:], start=5):  # 保留最新的5个
            old_log.unlink()

    # 生成带时间戳的新日志文件名
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"game_{timestamp}.log"

    # 清除所有现有处理器
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()

    # 文件处理器（每次运行新建文件）
    file_handler = logging.FileHandler(
        filename=log_file,
        mode='w',  # 每次覆盖新建
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter('[%(levelname)s] %(asctime)s [%(name)s] - %(message)s')
    )

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if os.getenv('DEBUG') else logging.INFO)
    console_handler.setFormatter(
        logging.Formatter('[%(levelname)s] %(name)s - %(message)s')
    )

    # 配置根日志器
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # 执行日志轮转
    rotate_logs()

    # 抑制第三方库日志
    logging.getLogger('arcade').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)

    # 记录本次日志文件信息
    root_logger.info(f"initialized logging, log file: {log_file.name}")

# 自动初始化
setup_logging()
logger = logging.getLogger(__name__)