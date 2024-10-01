import os
import re
import json
from src.utils.process_utils import get_all_comments, getToday
from src.utils.logging_utils import logger
from src.services.process.comment_process import add_language_to_comment, pick_necessary_data_points, add_details_comments
from src.services.process.training import preprocess_comments
from src.constant import iso_file_format_date


def has_code_snippet(comment_body):
    if not comment_body:
        return False

    """
    Check if the comment body contains a code snippet.

    """
    # Regular expression to detect code snippets wrapped in backticks (`` ` ``)
    code_snippet_pattern = r'`[^`]+`'

    # Check if the comment body contains any code snippet
    return re.search(code_snippet_pattern, comment_body) is not None


def filter_noise(comments):
    filter_commets = []
    logger.info(
        "started filterig noise from comments having comments length more than 100 characters")
    if len(comments):
        for comment in comments:
            if has_code_snippet(comment["body"]):
                filter_commets.append(comment)
    logger.info(
        f"completed filtering out noise from comments: Filtered comments {len(filter_commets)}")
    return filter_commets


def dump_data(comments):
    logger.info(
        "adding processed comments to output file")
    os.makedirs(f"data/{getToday(iso_file_format_date)}", exist_ok=True)
    processed_json_path = os.path.join(
        f"data/{getToday(iso_file_format_date)}", "output.json")
    with open(processed_json_path, 'w+') as f:
        json.dump(comments, f, indent=2)
    logger.info(
        "completed adding processed comments to output file")


def process():
    comments = get_all_comments()
    original_comments_length = len(comments)
    comments = filter_noise(comments)
    comments = add_language_to_comment(comments)
    comments = add_details_comments(comments)
    comments = pick_necessary_data_points(comments)
    comments = preprocess_comments(comments)
    logger.info(f"Total comments fetched are {
                original_comments_length} and final output got {len(comments)}")
    dump_data(comments)
