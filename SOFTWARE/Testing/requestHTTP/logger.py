import logging
from datetime import datetime
import os

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
log_filename = datetime.now().strftime("scan_log_%Y-%m-%d_%H-%M-%S.log")
log_filepath = os.path.join(desktop_path, log_filename)

logging.basicConfig(filename=log_filepath, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_message(message):
    logging.info(message)
