import logging
import os
from src.utils.utils import getToday
from src.constant import iso_format_date, iso_format_date_time


# Create logs directory if it doesn't exist
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Path for the log file
log_file_path = os.path.join(log_dir, "scraper.log")

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,  # Set log level to INFO or DEBUG based on requirement
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.FileHandler(log_file_path),  # Log to a file
        logging.StreamHandler()  # Log to the console (terminal)
    ],
    datefmt=iso_format_date_time  # Timestamp format
)

# Create a logger instance
logger = logging.getLogger(__name__)
