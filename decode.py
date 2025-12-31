import requests
import re

DOC_URL = "https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9DIz-vaHiHN02TKgDi7jy4ZpTpNqM7EvEcfr_p/pub"


def fetch_doc_text(doc_url: str) -> str:
    """
    Fetch the Google Doc as plain text using the export endpoint.
    """
    # Extract document ID
    doc_id = doc_url.split("/d/")[1].split("/")[0]

    # Plain-text export URL
    txt_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"

    response = requests.get(txt_url, timeout=20)
    response.raise_for_status()
    return response.text


def decode_secret_message(doc_url: str):
    """
    Retrieves character coordinate data from a Google Doc and prints
    the decoded grid message.
    """
    text = fetch_doc_text(doc_url)

    # Pattern: (x, y) CHARACTER
    pattern = re.compile(r"\((\d+),\s*(\d+)\)\s+(.+)")

    points = []
    max_x = 0
    max_y = 0

    for line in text.splitlines():
        match = pattern.search(line)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            char = match.group(3)

            points.append((x, y, char))
            max_x = max(max_x, x)
            max_y = max(max_y, y)

    # Initialize grid with spaces
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Place characters
    for x, y, char in points:
        grid[y][x] = char

    # Print result
    for row in grid:
        print("".join(row))


if __name__ == "__main__":
    decode_secret_message(DOC_URL)