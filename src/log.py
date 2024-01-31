import logging
import colorlog
import sys


def LogPrint(LogPrints):
    try:
        # 创建日志记录器
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.WARNING)

        logger.handlers.clear()

        # 创建控制台处理器并设置日志级别
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)

        # stream_handler = logging.StreamHandler()
        # stream_handler.setLevel(logging.WARNING)

        # 创建格式化器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s' + ' - ' + LogPrints)


        log_colors = {
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'purple'
        }

        # PrintStr = colorlog.ColoredFormatter(formatter, log_colors=log_colors)
        # stream_handler.setFormatter(PrintStr)
        # logger.addHandler(stream_handler)

        # 将格式化器添加到控制台处理器
        console_handler.setFormatter(formatter)

        # 将控制台处理器添加到日志记录器
        logger.addHandler(console_handler)
        #
        # 记录日志信息
        # logger.debug('debug message')
        # logger.info('info message')
        logger.warning('warning message')
        # logger.error('error message')
        # logger.critical('critical message')
    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")
