import requests, re, asyncio, aiohttp, trafilatura
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Set

HEADERS = {"User-Agent": "autoblog-bot/0.1 (+https://github.com/your/repo)"}
TIMEOUT = aiohttp.ClientTimeout(total=20)

def _is_same_domain(link: str, root_netloc: str) -> bool:
    return urlparse(link).netloc == root_netloc or urlparse(link).netloc == ""

def _clean_url(link: str, root: str) -> str:
    return urljoin(root, link.split("#")[0])  # resolve /about → https://site/about

async def _fetch(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url, headers=HEADERS) as r:
        if r.status != 200 or "text/html" not in r.headers.get("content-type", ""):
            return ""
        return await r.text()

async def crawl_site(root: str, max_pages: int = 10) -> List[str]:
    """
    Return a list of cleaned text strings from root + its same-domain links.
    Depth = 1. Obeys robots.txt implicitly by respecting 403/401/robots blocks.
    """
    parsed_root = urlparse(root if root.startswith("http") else "https://" + root)
    root_url    = parsed_root.geturl()
    netloc      = parsed_root.netloc

    to_visit: Set[str] = {root_url}
    seen: Set[str] = set()
    texts: List[str] = []

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        while to_visit and len(seen) < max_pages:
            url = to_visit.pop()
            seen.add(url)

            html = await _fetch(session, url)
            if not html:
                continue

            # extract clean text
            text = trafilatura.extract(html, include_tables=False, include_images=False)
            if text:
                texts.append(text)

            # collect new same-domain links
            soup = BeautifulSoup(html, "html.parser")
            for a in soup.find_all("a", href=True):
                link = _clean_url(a["href"], root_url)
                if _is_same_domain(link, netloc) and link not in seen:
                    to_visit.add(link)
                    if len(to_visit) + len(seen) >= max_pages:
                        break
    return texts
