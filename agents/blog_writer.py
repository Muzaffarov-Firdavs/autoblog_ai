from openai import AsyncOpenAI
from .base import BaseAgent

client = AsyncOpenAI()

class BlogWriterAgent(BaseAgent):
    async def run(self, outline: str, topic: str, prompt: str = ""):
        system = ("You are an engaging blog writer. Expand each heading (~150 words), "
                  "use second-person voice, embed '{{YOUTUBE_LINK}}' once, "
                  "and leave a '{{SOURCE_LINKS}}' placeholder at the end.")
        user = f"Topic: {topic}\nExtra guidance: {prompt}\nOutline:\n{outline}"
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":system},
                      {"role":"user","content":user}]
        )
        return {"draft_md": resp.choices[0].message.content.strip()}
