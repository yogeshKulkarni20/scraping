import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from src.utils.logging_utils import logger


stop_words = set(stopwords.words("english"))


def clean_comment(text):
    logger.info(
        f"cleaning comment by removing unnecessary characters and lowercasing")
    """
    Clean the body (comment) by removing unnecessary characters and lowercasing.
    """
    # Remove code snippets wrapped in backticks
    text = re.sub(r'`[^`]+`', '', text)
    # Remove non-alphanumeric characters except spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Lowercase the text
    text = text.lower()
    # Tokenize and remove stopwords
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    logger.info(
        "cleaning completed for comment by removing unnecessary characters and lowercasing")
    return ' '.join(words)


def clean_code(code):
    logger.info(
        "cleaning code for before and after diff hunk by removing extra whitespaces and normalizing the syntax")

    """
    Clean the code by removing extra whitespaces and normalizing the syntax.
    """
    # Normalize spaces and line breaks
    code = re.sub(r'\s+', ' ', code).strip()
    # Remove extra comments or unnecessary symbols (optional)
    code = re.sub(r'/\*.*?\*/', '', code)  # Example for multiline comments
    logger.info(
        "cleaning code completed for before and after diff hunk by removing extra whitespaces and normalizing the syntax")

    return code


def preprocess_comments(comments):
    """
    Preprocess the JSON data for better model input:
    - Clean the comments
    - Tokenize the code before and after changes
    - Handle language-specific preprocessing
    """
    preprocessed_comments = []

    for comment in comments:
        clean_body = clean_comment(comment['body'])
        clean_code_before = clean_code(comment['code_before'])
        clean_code_after = clean_code(comment['code_after'])

        preprocessed_comments.append({
            'comment': clean_body,
            'language': comment['language'],
            'code_before': clean_code_before,
            'code_after': clean_code_after
        })

    return preprocessed_comments
