import os
import json
from src.utils.utils import getToday
from src.utils.logging_utils import logger
from src.constant import iso_file_format_date


def get_all_comments():
    file_path = os.path.join(
        f"./data/{getToday(iso_file_format_date)}", "output.json")
    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON in {
                file_path}: {str(e)}")
