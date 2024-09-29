import asyncio
from src.constant import timeout


async def rate_limited_request():
    """
    Introduce a delay between requests to adhere to GitHub API rate limits.
    """
    await asyncio.sleep(timeout)
