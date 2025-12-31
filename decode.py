import re
import requests

DOC_URL = "https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9DIz-vaHiHN02TKgDi7jy4ZpTpNqM7EvEcfr_p/pub"

def decode_secret_message(doc_url: str):
    # Try a text-friendly output first (often works better than HTML for published docs)
    candidates = [
        doc_url + "?output=txt",
        doc_url,
    ]

    text = None
    for u in candidates:
        r = requests.get(u, timeout=20)
        if r.ok and r.text.strip():
            text = r.text
            break

    if text is None:
        raise RuntimeError("Could not fetch document")

    # Extract "(x, y) char" lines
    pattern = re.compile(r"\((\d+),\s*(\d+)\)\s+(.+)$")

    points = []
    max_x = max_y = 0
    for line in text.splitlines():
        m = pattern.search(line)
        if m:
            x = int(m.group(1))
            y = int(m.group(2))
            ch = m.group(3)
            points.append((x, y, ch))
            max_x = max(max_x, x)
            max_y = max(max_y, y)

    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y, ch in points:
        grid[y][x] = ch

    for row in grid:
        print("".join(row))

if __name__ == "__main__":
    decode_secret_message(DOC_URL)