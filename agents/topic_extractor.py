from openai import AsyncOpenAI
from .base import BaseAgent
import textwrap

client = AsyncOpenAI()

class TopicExtractorAgent(BaseAgent):
    async def run(self, site_corpus: str, n_topics: int = 8):
        # Trim to ~15 k chars to fit GPT-4o context safely
        corpus = textwrap.shorten(site_corpus, width=15000, placeholder="[…]")

        system = "You are a content strategist. Extract key themes users care about."
        user   = f"Website corpus:\n{corpus}\n\nReturn {n_topics} bullet points."

        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":system},
                {"role":"user","content":user}
            ]
        )
        topics = [l.strip("•- ") for l in resp.choices[0].message.content.splitlines() if l.strip()]
        return {"topics": topics[:n_topics]}
