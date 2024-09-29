import os
from src.utils.utils import getToday
from src.api.s3 import upload_file_to_s3
from src.utils.logging_utils import logger
from src.constant import repo_updated_list, iso_file_format_date


def uploadComments() -> None:
    todayStr = getToday(iso_file_format_date)
    rootDir = f"data/{todayStr}/"
    all_combined_file_name = "output.json"
    all_combined_file_path = os.path.join(
        rootDir, all_combined_file_name)

    try:
        if os.path.exists(all_combined_file_path):
            """ Upload all combined file to that """
            s3FilePathForAll = f"data/{todayStr}/output.json"
            logger.info(
                f"started uploading all comments data across repos @ {s3FilePathForAll}")
            upload_file_to_s3(all_combined_file_path, s3FilePathForAll)
            logger.info(
                f"upload completed for all comments data across repos @ {s3FilePathForAll}")
            logger.info("uploading all languages comment info")
            for root, dir, files in os.walk(f"data/{todayStr}/languages"):
                for file in files:
                    logger.info(f"uploading file {file} comment info")
                    s3FilePathForRepo = f"data/{todayStr}/languages/{file}"
                    currentFilePath = os.path.join(
                        f"data/{todayStr}/languages", file)
                    upload_file_to_s3(currentFilePath,
                                      s3FilePathForRepo)
                    logger.info(f"completed uploading file {
                                file} comment info")
            logger.info("uploading completed for all languages comment info")
    except Exception as e:
        logger.error(f"error while upoading files: {str(e)}")


def uploadLogs():
    todayStr = getToday(iso_file_format_date)
    pathname = f"logs/scraper.log"
    """ Upload all combined logs to that """
    try:
        if os.path.exists(pathname):
            s3LogPath = f"logs/{todayStr}.log"
            logger.info(
                f"started uploading all logs data @ {s3LogPath} on {todayStr}")
            upload_file_to_s3(pathname, s3LogPath)
            logger.info(
                f"upload completed for logs data @ {s3LogPath} on {todayStr}")
    except Exception as e:
        logger.error(
            f"error while upoading logger file @{s3LogPath} on {todayStr}: {str(e)}")


def upload():
    uploadComments()
    uploadLogs()
