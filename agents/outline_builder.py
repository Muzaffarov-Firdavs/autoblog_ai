from openai import AsyncOpenAI
from .base import BaseAgent

client = AsyncOpenAI()

class OutlineBuilderAgent(BaseAgent):
    async def run(self, bullets: str, topic: str, prompt: str = ""):
        system = ("You are a senior content strategist obeying Google E-E-A-T and "
                  "'helpful content' guidelines. Build an H-tag outline.")
        user = (f"Topic: {topic}\nExtra instructions: {prompt}\n"
            f"Key facts:\n{bullets}\n\nReturn an H-tag outline …")
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":system},
                      {"role":"user","content":user}]
        )
        outline_md = resp.choices[0].message.content.strip()
        return {"outline": outline_md}
