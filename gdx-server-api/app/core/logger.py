# app/core/logger.py
import logging
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# ----------------------------
# Handlers
# ----------------------------
access_handler = logging.FileHandler("logs/access.log", encoding="utf-8")
error_handler = logging.FileHandler("logs/error.log", encoding="utf-8")
warning_handler = logging.FileHandler("logs/warning.log", encoding="utf-8")
console_handler = logging.StreamHandler()

# ----------------------------
# Levels
# ----------------------------
access_handler.setLevel(logging.INFO)
error_handler.setLevel(logging.ERROR)
warning_handler.setLevel(logging.WARNING)
console_handler.setLevel(logging.DEBUG)

# ----------------------------
# Formatter
# ----------------------------
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
for handler in [access_handler, error_handler, warning_handler, console_handler]:
    handler.setFormatter(formatter)

# ----------------------------
# Loggers
# ----------------------------
root_logger = logging.getLogger("app")
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(console_handler)

# Separate loggers
access_logger = logging.getLogger("app.access")
access_logger.setLevel(logging.INFO)
access_logger.addHandler(access_handler)
access_logger.propagate = False

error_logger = logging.getLogger("app.error")
error_logger.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)
error_logger.propagate = False

warning_logger = logging.getLogger("app.warning")
warning_logger.setLevel(logging.WARNING)
warning_logger.addHandler(warning_handler)
warning_logger.propagate = False

__all__ = ["root_logger", "access_logger", "error_logger", "warning_logger"]
