import os
import asyncio
import aiohttp
import random
import time
from dotenv import load_dotenv
from src.api.github import fetch_comments_per_page
from src.utils.file_utils import saveResponseToFile
from src.utils.github_utils import get_last_page
from src.utils.logging_utils import logger
from src.constant import github_comments_api_prefix, repo_updated_list

load_dotenv()

GITHUB_ACCESS_TOKEN_1 = os.getenv('GITHUB_ACCESS_TOKEN_1')
GITHUB_ACCESS_TOKEN_2 = os.getenv('GITHUB_ACCESS_TOKEN_2')
GITHUB_ACCESS_TOKEN_3 = os.getenv('GITHUB_ACCESS_TOKEN_3')


async def fetch_all_comments_per_repo(session, owner, repo, headers):
    """
    Fetch all PR comments for a given repository, handling pagination.
    """
    try:
        github_url = f"{
            github_comments_api_prefix}/{owner}/{repo}/pulls/comments"
        logger.info(f"Fetching PR comments for repo {owner}/{repo}")

        start_time = time.time()  # Record start time

        first_page_comments_data = await fetch_comments_per_page(session, github_url, 1, headers)
        if first_page_comments_data["data"] is None:
            return

        saveResponseToFile(
            owner, repo, 1, first_page_comments_data["data"])

        total_pages = 1

        if "link" in first_page_comments_data["headers"]:
            total_pages = get_last_page(
                first_page_comments_data["headers"]["link"])

        logger.info(f"Total pages available: {total_pages}")

        tasks = []
        for page in range(2, total_pages + 1):
            tasks.append(fetch_comments_per_page(
                session, github_url, page, headers))

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for page_num, comments in enumerate(responses, start=2):
            if comments["data"]:
                saveResponseToFile(owner, repo, page_num, comments["data"])

        end_time = time.time()  # Record start time
        elapsed_time = end_time - start_time  # Total time taken for repo

        # Log the total execution time
        logger.info(f"Completed fetching comments for repo {
                    owner}/{repo} in {elapsed_time:.2f} seconds.")

    except Exception as e:
        logger.error(f"Error fetching comments for {owner}/{repo}: {str(e)}")


async def concurrent_repos_data():
    """
    Create concurrent tasks for fetching comments from multiple repositories.
    """
    start_time = time.time()  # Record start time

    async with aiohttp.ClientSession() as session:
        tasks = []
        for repo_details in repo_updated_list:
            accessToken = random.choice(
                [GITHUB_ACCESS_TOKEN_1, GITHUB_ACCESS_TOKEN_2, GITHUB_ACCESS_TOKEN_3])
            HEADERS = {
                "Authorization": f"Bearer {accessToken}",
                "Accept": "application/vnd.github+json"
            }
            tasks.append(fetch_all_comments_per_repo(
                session, repo_details["owner"], repo_details["repo"], HEADERS))

        results = await asyncio.gather(*tasks, return_exceptions=True)

    # Calculate execution time
    end_time = time.time()
    elapsed_time = end_time - start_time  # Total time taken

    # Log the total execution time
    logger.info(f"Scraping completed in {elapsed_time:.2f} seconds.")

    return results
