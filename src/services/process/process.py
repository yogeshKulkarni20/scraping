import os
import json
from src.utils.process_utils import get_all_comments, getToday
from src.utils.logging_utils import logger
from src.services.process.comment_process import add_language_to_comment, pick_necessary_data_points, add_details_comments
from src.services.process.training import preprocess_comments
from src.constant import iso_file_format_date


def filter_noise(comments):
    filter_commets = []
    logger.info(
        "started filterig noise from comments having comments length more than 100 characters")
    if len(comments):
        for comment in comments:
            if comment["body"] and len(comment["body"].strip()) >= 100:
                filter_commets.append(comment)
    logger.info(
        "completed filtering out noise from comments")
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
    comments = filter_noise(comments)
    comments = add_language_to_comment(comments)
    comments = add_details_comments(comments)
    comments = pick_necessary_data_points(comments)
    comments = preprocess_comments(comments)
    len(comments)
    dump_data(comments)
