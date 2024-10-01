import asyncio
from src.services.scraper import concurrent_repos_data
from src.services.collect import collect
from src.services.upload import upload
from src.services.delete import delete
from src.services.process.process import process
from src.utils.logging_utils import logger


def scrape():
    """
    Entry point for the scraping process.
    """
    logger.info("Starting scraping process")
    asyncio.run(concurrent_repos_data())
    logger.info("Scraping process completed")


if __name__ == "__main__":
    scrape()
    collect()
    process()
    upload()
    delete()
