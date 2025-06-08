import asyncio
from dotenv import load_dotenv; load_dotenv()

from agents.query_generator  import QueryGeneratorAgent
from agents.researcher       import ResearcherAgent
from agents.summariser       import SummariserAgent
from agents.outline_builder  import OutlineBuilderAgent
from agents.blog_writer      import BlogWriterAgent
from agents.grammar_checker  import GrammarCheckerAgent
from agents.file_publisher   import FilePublisherAgent
from agents.source_linker    import SourceLinkerAgent
from agents.website_crawler  import WebsiteCrawlerAgent
from agents.topic_extractor  import TopicExtractorAgent
from utils.youtube import search_video_embed


async def pipeline(topic: str, user_prompt: str, site: str | None):
    crawl_bot  = WebsiteCrawlerAgent("Crawler")
    topic_bot  = TopicExtractorAgent("Topics")
    linker_bot  = SourceLinkerAgent("Links")
    kw_bot   = QueryGeneratorAgent("Keywords")
    research_bot = ResearcherAgent("Research")
    summarise_bot = SummariserAgent("Summarise")
    outline_bot   = OutlineBuilderAgent("Outline")
    write_bot     = BlogWriterAgent("Writer")
    proof_bot     = GrammarCheckerAgent("Proof")
    file_bot      = FilePublisherAgent("FileOut")


    if site:
        corpus     = await crawl_bot.run(site=site)
        topics_out = await topic_bot.run(site_corpus=corpus["site_corpus"])
        extracted_topics = "; ".join(topics_out["topics"])
        user_prompt = f"{user_prompt}\n\nWebsite themes to cover: {extracted_topics}".strip()

    kws   = await kw_bot.run(topic=topic, prompt=user_prompt)
    serp  = await research_bot.run(keywords=kws["keywords"])
    facts = await summarise_bot.run(serp_data=serp["serp_data"])
    outline = await outline_bot.run(bullets=facts["bullets"], topic=topic, prompt=user_prompt)
    draft = await write_bot.run(outline=outline["outline"], topic=topic, prompt=user_prompt)
    links = await linker_bot.run(serp_data=serp["serp_data"])
    final = await proof_bot.run(draft_md=draft["draft_md"])

    embed = search_video_embed(topic)
    filled = (final["final_md"]
              .replace("{{YOUTUBE_LINK}}", embed)
              .replace("{{SOURCE_LINKS}}", links["sources_markdown"]))

    published = file_bot.run(title=topic, markdown=filled)
    return published["file_path"]


if __name__ == "__main__":
    print("Enter the website URL to scrap for topics (or leave blank to skip):")
    site = input("Website URL: ").strip()
    topic = input("Enter blog topic: ").strip()
    user_prompt = input("Enter extra writing guidance (optional): ").strip()
    path  = asyncio.run(pipeline(topic, user_prompt, site))
    print(f"✅ Blog saved to {path}")
