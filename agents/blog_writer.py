from openai import AsyncOpenAI
from .base import BaseAgent

client = AsyncOpenAI()

class BlogWriterAgent(BaseAgent):
    async def run(self, outline: str, topic: str):
        system = ("You are an engaging blog writer. Expand each heading into ≈150 words, "
                  "use second-person voice, embed '{{YOUTUBE_LINK}}' once where relevant, "
                  "and keep Markdown.")
        user = f"Outline:\n{outline}\n\nWrite full post."
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":system},
                      {"role":"user","content":user}]
        )
        return {"draft_md": resp.choices[0].message.content.strip()}
