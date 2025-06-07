from openai import AsyncOpenAI
from .base import BaseAgent

client = AsyncOpenAI()

class GrammarCheckerAgent(BaseAgent):
    async def run(self, draft_md: str):
        system = "You are a meticulous proof-reader. Fix grammar, typos, and clarity."
        user   = draft_md + "\n\nReturn corrected Markdown only."
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":system},
                      {"role":"user","content":user}]
        )
        return {"final_md": resp.choices[0].message.content.strip()}
