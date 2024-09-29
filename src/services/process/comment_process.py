import re
import os
from src.services.process.constant import file_extension_to_language, data_points_to_use
from src.utils.logging_utils import logger


def get_language_from_path(file_path):
    extension = os.path.splitext(file_path)[1]
    return file_extension_to_language.get(extension, "Unknown")


def add_language_to_comment(comments):
    updatedComments = []
    for comment in comments:
        if "path" in comment:
            language = get_language_from_path(comment.get("path"))
            comment["language"] = language
            updatedComments.append(comment)
    return updatedComments


def pick_necessary_data_points(comments):
    updatedComments = []
    for comment in comments:
        updatedComment = {}
        for key, value in comment.items():
            if key in data_points_to_use:
                updatedComment[key] = value
        updatedComments.append(updatedComment)
    return updatedComments


def process_complex_diff_hunk(diff_hunk):
    """
    Process a complex diff hunk into 'code before' and 'code after',
    and add the associated comment. Handles multiple diff blocks.

    Parameters:
    diff_hunk (str): The diff hunk string.
    comment (str): The review comment associated with the diff hunk.

    Returns:
    dict: A dictionary containing 'code_before', 'code_after', and 'comment'.
    """
    # Split the hunk into individual lines
    lines = diff_hunk.split('\n')

    code_before = []
    code_after = []
    code_context = []

    for line in lines:
        # Removed lines start with '-'
        if line.startswith('-'):
            code_before.append(line[1:].strip())
        # Added lines start with '+'
        elif line.startswith('+'):
            code_after.append(line[1:].strip())
        # Context lines (unchanged lines) appear in both before and after
        elif line.startswith(' '):
            stripped_line = line.strip()
            code_before.append(stripped_line)
            code_after.append(stripped_line)
        # Lines starting with @@ are metadata that indicate a new diff block
        elif line.startswith('@@'):
            # You can extract line numbers if needed using regex from diff metadata
            match = re.match(r'@@ -(\d+),\d+ \+(\d+),\d+ @@', line)
            if match:
                before_line_num = int(match.group(1))
                after_line_num = int(match.group(2))
                # Optionally, track line numbers for more advanced use cases
                code_context.append(
                    f"Line {before_line_num} -> {after_line_num}")

    # Join the code before and after into single strings
    code_before_str = '\n'.join(code_before)
    code_after_str = '\n'.join(code_after)

    return {
        "code_before": code_before_str,
        "code_after": code_after_str,
        "context": code_context
    }


""" Not being used for now """


def get_code_suggestion(comment_body: str):
    """
    Extract code suggestions and return the cleaned comment without code snippets.

    Parameters:
    comment_body (str): The text of the comment.

    Returns:
    tuple: A tuple containing:
           - A list of code suggestions.
           - The comment body with code suggestions removed.
    """
    # Regex pattern to match code snippets wrapped in backticks (`...` or ```...```)
    code_snippet_pattern = r'`([^`]+)`|```([^`]+)```'

    # Extract all code snippets from the comment
    code_suggestions = re.findall(code_snippet_pattern, comment_body)

    # Flatten the result from the regex (as it returns a tuple for each match)
    code_suggestions = [
        snippet for pair in code_suggestions for snippet in pair if snippet]

    # Remove code snippets from the comment body
    comment_text = re.sub(code_snippet_pattern, '', comment_body)

    # Remove any extra spaces and newlines left behind
    comment_text = comment_text.strip()

    return {"code_suggestions": code_suggestions, "comment_text": comment_text}


def add_details_comments(comments):
    updatedComments = []
    logger.info("processing diff hunk details for code before and afte text")
    for comment in comments:
        if comment["diff_hunk"]:
            details = process_complex_diff_hunk(
                comment["diff_hunk"])
            updatedComment = {**comment, **details}
            updatedComments.append(updatedComment)
    logger.info(
        "processing completed for diff hunk details for code before and afte text")
    return updatedComments
