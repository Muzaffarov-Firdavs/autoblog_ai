from pathlib import Path
import datetime, re
from .base import BaseAgent

MEDIA_DIR = Path(__file__).resolve().parent.parent / "media"
MEDIA_DIR.mkdir(exist_ok=True)

def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)

class FilePublisherAgent(BaseAgent):
    def run(self, title: str, markdown: str):
        now   = datetime.datetime.now().strftime("%Y%m%d")
        slug  = slugify(title)
        path  = MEDIA_DIR / f"{now}-{slug}.md"
        path.write_text(markdown, encoding="utf-8")
        return {"file_path": str(path)}
