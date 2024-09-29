import asyncio
import aiohttp
from src.utils.logging_utils import logger
from src.utils.rate_limiter import rate_limited_request
from src.utils.utils import getLastNthDay
from src.constant import per_page_comments, duration_in_days, max_retries, timeout


async def fetch_comments_per_page(session, github_url, page, headers, retries=0):
    """
    Fetch a single page of PR comments from GitHub API asynchronously.
    Retries up to MAX_RETRIES on failure.
    """
    logger.info(f"Fetching PR comments from {github_url}, page: {page}")
    since = getLastNthDay(duration_in_days)

    try:
        await rate_limited_request()

        async with session.get(github_url, params={
            "since": since,
            "page": page,
            "per_page": per_page_comments,
        }, headers=headers, timeout=timeout) as response:

            if response.status == 200:
                logger.info(f"Successfully fetched page {
                            page} from {github_url}")
                commentsData = await response.json()
                return {
                    "data": commentsData,
                    "headers": response.headers
                }

            logger.error(f"Failed to fetch data from {github_url}, page {
                         page}. Status: {response.status}")

            if response.status >= 500 and retries < max_retries:
                logger.warning(f"Retrying... Attempt {
                               retries + 1}/{max_retries}")
                return await fetch_comments_per_page(session, github_url, page, headers, retries + 1)

            return None

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        logger.error(f"Error fetching from {
                     github_url}, page {page}: {str(e)}")
        if retries < max_retries:
            return await fetch_comments_per_page(session, github_url, page, headers, retries + 1)
        return None
