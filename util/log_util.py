import logging
import os
import sys
from datetime import datetime
from pathlib import Path


# 定义ANSI颜色代码
class Colors:
    BLACK = '\033[30m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'


class StLogger:
    """彩色日志工具类"""

    def __init__(self, name=None):
        """
        初始化日志记录器
        Args:
            name: 日志记录器名称，通常使用 __name__
        """
        # 获取调用者的模块名称
        if name is None:
            # 这里可以自动获取调用者的模块信息
            name = self._get_caller_module()

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 避免重复添加handler
        if not self.logger.handlers:
            self._setup_handlers()

    def _get_caller_module(self):
        """获取调用者的模块信息"""
        import inspect
        # 获取调用栈，找到第一个不是本文件的调用者
        frame = inspect.currentframe()
        try:
            # 向上追溯调用栈
            while frame:
                frame = frame.f_back
                if frame and frame.f_globals.get('__name__') != __name__:
                    module_name = frame.f_globals.get('__name__', 'unknown')
                    filename = frame.f_globals.get('__file__', 'unknown')
                    return f"{module_name}({os.path.basename(filename)})"
        finally:
            del frame
        return 'unknown'

    def _setup_handlers(self):
        """设置处理器和格式器"""
        # 创建控制台处理器
        if self.logger.handlers:
            # 如果已有handler，直接返回
            return

        # 关键设置：阻止日志向父logger传播
        self.logger.propagate = False

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        # 创建彩色格式器 - 包含文件名和行号
        class ColoredFormatter(logging.Formatter):
            """自定义彩色格式器"""

            # 定义不同日志级别的颜色映射
            LEVEL_COLORS = {
                logging.DEBUG: Colors.CYAN,
                logging.INFO: Colors.BLACK,
                logging.WARNING: Colors.YELLOW,
                logging.ERROR: Colors.RED,
                logging.CRITICAL: Colors.RED + '\033[1m'  # 粗体红色
            }

            def format(self, record):
                # 获取对应级别的颜色
                level_color = self.LEVEL_COLORS.get(record.levelno, Colors.RESET)
                reset_color = Colors.RESET

                # 创建基础格式器
                base_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )

                # 格式化日志记录
                formatted_message = base_formatter.format(record)

                # 添加颜色
                colored_message = f"{level_color}{formatted_message}{reset_color}"
                return colored_message

        # 设置格式器
        formatter = ColoredFormatter()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 文件日志:项目根目录/log/skp_YYYYMMDD.log(UTF-8)
        log_dir = Path(__file__).resolve().parent.parent / 'log'
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            log_dir / f"skp_{datetime.now().strftime('%Y%m%d')}.log", encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)

    # 日志方法
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)


# 创建全局实例（可选）
# _default_logger = StLogger('GlobalLogger')


# 便捷函数
def get_logger(name=None):
    """获取日志记录器的便捷函数"""
    return StLogger(name)


# 测试代码
if __name__ == "__main__":
    # 测试当前模块
    logger = StLogger(__name__)
    logger.debug("这是一条调试信息")
    logger.info("这是一条普通信息")
    logger.warning("这是一条警告信息")
    logger.error("这是一条错误信息")
    logger.critical("这是一条严重错误信息")
