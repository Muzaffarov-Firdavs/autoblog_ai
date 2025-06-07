from openai import AsyncOpenAI
from .base import BaseAgent
import textwrap, json

client = AsyncOpenAI()

class SummariserAgent(BaseAgent):
    async def run(self, serp_data):
        # Flatten snippets for GPT context
        passages = []
        for kw in serp_data:
            for item in kw["results"][:5]:          # keep top‐5 per keyword
                passages.append(f"- {item['title']}: {item['snippet']}")
        corpus = "\n".join(passages)

        system = "You are a diligent researcher. Extract factual bullet points."
        user   = f"Source snippets:\n{corpus}\n\nReturn <=10 bullet points."
        resp   = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":system},
                      {"role":"user","content":textwrap.shorten(user, 12000)}]
        )
        bullets = resp.choices[0].message.content.strip()
        return {"bullets": bullets}
