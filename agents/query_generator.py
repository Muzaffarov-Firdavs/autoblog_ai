from openai import AsyncOpenAI
from .base import BaseAgent

client = AsyncOpenAI()

class QueryGeneratorAgent(BaseAgent):
    async def run(self, topic: str, n: int = 5):
        system = "You are an SEO expert. Generate long-tail keywords."
        user   = f"Topic: {topic}\nReturn {n} comma-separated keywords."
        resp   = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":system},
                      {"role":"user","content":user}]
        )
        kws = [k.strip() for k in resp.choices[0].message.content.split(",")]
        return {"keywords": kws[:n]}
