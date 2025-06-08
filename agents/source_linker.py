from urllib.parse import urlparse
from textwrap import shorten
from .base import BaseAgent

def _favicon(domain: str, size: int = 32) -> str:
    return f"https://www.google.com/s2/favicons?domain={domain}&sz={size}"

class SourceLinkerAgent(BaseAgent):
    """
    Produce Markdown list items that show a favicon + linked title.
    Input: serp_data = [{keyword, results:[{title, link, ...}, …]}, …]
    Output: {"sources_markdown": "## Sources\n- <img …> [Title](URL)\n …"}
    """
    async def run(self, serp_data: list, max_sources: int = 10):
        seen, lines = set(), []
        for kw in serp_data:
            for item in kw["results"]:
                url   = item["link"]
                domain = urlparse(url).netloc.replace("www.", "")
                if domain in seen:
                    continue
                seen.add(domain)
                icon = _favicon(domain)
                title = shorten(item["title"], width=60, placeholder="…")
                md = f'- <img src="{icon}" width="16" height="16" style="vertical-align:middle;"> ' \
                     f'[{title}]({url})'
                lines.append(md)
                if len(lines) == max_sources:
                    break
            if len(lines) == max_sources:
                break
        block = "## Sources\n" + "\n".join(lines) if lines else ""
        return {"sources_markdown": block}
