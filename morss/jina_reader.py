import os
import urllib.request
import lxml.html
import mistune


def get_article(url: str, format: str = "markdown") -> str:
    if format not in ["markdown", "html"]:
        raise ValueError(f"Unsupported format: {format}")
    headers = {
        "X-Return-Format": format,
        "User-Agent": "python-requests/2.25.0",
    }
    if os.getenv("JINA_AI_TOKEN"):
        headers["Authorization"] = f"Bearer {os.getenv('JINA_AI_TOKEN')}"

    url = f"https://r.jina.ai/{url}"
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request, timeout=10)
    content = response.read().decode("utf-8")

    if format == "markdown":
        return mistune.html(content)
    if format == "html":
        body = lxml.html.fromstring(content).xpath("//body")
        if not body:
            return content
        return lxml.html.tostring(body[0], encoding="unicode")


if __name__ == "__main__":
    import sys

    os.environ["JINA_AI_FORMAT"] = "html"

    url = sys.argv[1] if len(sys.argv) > 1 else "https://morss.it"
    article = get_article(url)

    if sys.flags.interactive:
        print(">>> Interactive shell: try using `article`")

    else:
        print(article)
