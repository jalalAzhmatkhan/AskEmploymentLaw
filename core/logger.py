import logging
from datetime import datetime
import os

from core.configs import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

current_date = datetime.now().strftime("%d-%m-%Y")
log_filename = f"{current_date}.log"
log_dir = settings.LOG_DIR
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
file_handler = logging.FileHandler(os.path.join(log_dir, log_filename))

formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)