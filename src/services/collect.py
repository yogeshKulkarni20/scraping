import os
import json
from collections import defaultdict
from src.utils.logging_utils import logger
from src.utils.utils import getToday
from src.constant import iso_file_format_date
from src.services.process.comment_process import add_language_to_comment


def combine_json_files_per_repo():
    all_repos_data = []  # This will store data across all repos

    for root, dirs, files in os.walk(f"data/{getToday(iso_file_format_date)}/"):
        repo_data = []
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    try:
                        # Read the JSON data from each file
                        data = json.load(f)
                        repo_data = repo_data+data
                        all_repos_data = all_repos_data+data  # Add to the global data
                    except json.JSONDecodeError as e:
                        logger.error(f"Error decoding JSON in {
                                     file_path}: {str(e)}")

        # Only proceed if there's data to combine for this repo
        if repo_data:
            # Create a combined JSON file for the repo
            repo_name = os.path.basename(root)
            combined_file_name = f"{repo_name}.json"
            combined_file_path = os.path.join(root, combined_file_name)

            # Write the combined data to the new file
            with open(combined_file_path, 'w') as f:
                json.dump(repo_data, f, indent=4)

            logger.info(f"Combined JSON data saved to {combined_file_path}")

    return all_repos_data  # Return the combined data for all repos


# Function to combine all repo data into a single file and upload to S3
def combine_all_repos_data(all_repos_data):
    # Create a combined JSON file for all repos
    currentDir = f"data/{getToday(iso_file_format_date)}/"
    all_combined_file_name = "output.json"
    all_combined_file_path = os.path.join(currentDir, all_combined_file_name)

    # Write the combined data for all repos to a file
    with open(all_combined_file_path, 'w') as f:
        json.dump(all_repos_data, f, indent=4)

    logger.info(f"Combined data for all repos saved to {
                all_combined_file_path}")


def classify_comments(comments):
    if not len(comments):
        return None
    classification = defaultdict(list)

    for comment in comments:
        language = comment["language"]
        classification[language].append(comment)

    for key, value in classification.items():
        os.makedirs(
            f"data/{getToday(iso_file_format_date)}/languages", exist_ok=True)
        currentDir = f"data/{getToday(iso_file_format_date)}/languages"
        file_name = f"{key}.json"
        language_data_path = os.path.join(
            currentDir, file_name)
        # Write the combined data for all repos to a file
        with open(language_data_path, 'w') as f:
            json.dump(value, f, indent=4)


def collect():
    all_repos_data = combine_json_files_per_repo()
    all_repos_data = add_language_to_comment(all_repos_data)
    classify_comments(all_repos_data)
    combine_all_repos_data(all_repos_data)
