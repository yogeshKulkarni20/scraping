import os
import json
from src.utils.logging_utils import logger
from src.utils.utils import getToday
from src.constant import iso_file_format_date


def saveResponseToFile(owner, repo, page, comments):
    """
    Save the comments response to a file for a given repository and page.
    """
    directory = f"data/{getToday(iso_file_format_date)}/{owner}/{repo}"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, f"comments_page_{page}.json")

    try:
        with open(file_path, "w") as file:
            json.dump(comments, file, indent=4)
        logger.info(f"Successfully saved comments to {file_path}")
    except Exception as e:
        logger.error(f"Error saving comments to {file_path}: {str(e)}")
