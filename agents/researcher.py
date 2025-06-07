from utils.serper import google_serp
from .base import BaseAgent

class ResearcherAgent(BaseAgent):
    async def run(self, keywords: list[str], per_kw: int = 10):
        bundle = []
        for kw in keywords:
            items = google_serp(kw, num=per_kw)
            bundle.append({"keyword": kw, "results": items})
        return {"serp_data": bundle}
