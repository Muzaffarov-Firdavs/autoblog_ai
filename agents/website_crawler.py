from .base import BaseAgent
from utils.crawl import crawl_site

class WebsiteCrawlerAgent(BaseAgent):
    async def run(self, site: str, max_pages: int = 10):
        texts = await crawl_site(site, max_pages=max_pages)
        # Concatenate for downstream LLMs (may truncate later)
        corpus = "\n\n".join(texts)
        return {"site_corpus": corpus}
