import re


def get_last_page(link_header):
    """
    Extract the last page number from the Link header.
    """
    # Use regex to find the URL for the rel="last" link
    match = re.search(r'<([^>]+)>;\s*rel="last"', link_header)

    if match:
        last_url = match.group(1)  # Get the URL part
        # Extract the page number from the last URL
        last_page = re.search(r'page=(\d+)', last_url)
        if last_page:
            # Return the page number as an integer
            return int(last_page.group(1))
    return None
