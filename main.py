import asyncio, os, sys
from dotenv import load_dotenv; load_dotenv()

from agents.query_generator import QueryGeneratorAgent
from agents.researcher       import ResearcherAgent
from agents.summariser       import SummariserAgent
from agents.outline_builder  import OutlineBuilderAgent
from agents.blog_writer      import BlogWriterAgent
from agents.grammar_checker  import GrammarCheckerAgent
from agents.file_publisher   import FilePublisherAgent
from utils.youtube import search_video_embed


async def pipeline(topic: str):
    kw_bot      = QueryGeneratorAgent("Keywords")
    research_bot = ResearcherAgent("Research")
    sum_bot     = SummariserAgent("Summarise")
    outline_bot = OutlineBuilderAgent("Outline")
    write_bot   = BlogWriterAgent("Writer")
    grammar_bot = GrammarCheckerAgent("Proof")
    file_bot    = FilePublisherAgent("FileOut")

    kws   = await kw_bot.run(topic=topic)
    serp  = await research_bot.run(keywords=kws["keywords"])
    facts = await sum_bot.run(serp_data=serp["serp_data"])
    outline = await outline_bot.run(bullets=facts["bullets"], topic=topic)
    draft   = await write_bot.run(outline=outline["outline"], topic=topic)
    final   = await grammar_bot.run(draft_md=draft["draft_md"])

    embed = search_video_embed(topic)
    final_html = final["final_md"].replace("{{YOUTUBE_LINK}}", embed)

    published = file_bot.run(title=topic, markdown=final_html)
    return published["file_path"]


if __name__ == "__main__":
    topic = input("Enter blog topic: ").strip()
    path  = asyncio.run(pipeline(topic))
    print(f"✅ Blog saved to {path}")
