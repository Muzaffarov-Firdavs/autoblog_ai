import os, requests, typing as t

_HOST = os.getenv("SERPER_HOST", "https://google.serper.dev")
_KEY  = os.getenv("SERPER_API_KEY")

_HEADERS = {"X-API-KEY": _KEY, "Content-Type": "application/json"}

def google_serp(query: str, num: int = 10) -> t.List[dict]:
    payload = {"q": query, "num": num}
    r = requests.post(f"{_HOST}/search", json=payload, headers=_HEADERS, timeout=20)
    r.raise_for_status()
    return r.json().get("organic", [])
