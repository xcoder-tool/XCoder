import sys

from loguru import logger

logger.remove()
logger.add(
    "./logs/info/{time:YYYY-MM-DD}.log",
    format="[{time:HH:mm:ss}] [{level}]: {message}",
    encoding="utf8",
    level="INFO",
)
logger.add(
    "./logs/errors/{time:YYYY-MM-DD}.log",
    format="[{time:HH:mm:ss}] [{level}]: {message}",
    backtrace=True,
    diagnose=True,
    encoding="utf8",
    level="ERROR",
)
logger.add(sys.stdout, format="<lvl>[{level}] {message}</lvl>", level="INFO")
