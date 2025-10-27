# filename: api/outline.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/")
def outline(country: str):
    wiki_url = f'https://en.wikipedia.org/wiki/{country.replace(" ", "_")}'
    resp = requests.get(wiki_url)
    if resp.status_code != 200:
        return {"error": f"Wikipedia page not found for {country}."}
    soup = BeautifulSoup(resp.text, "html.parser")
    headings = soup.find_all(['h1','h2','h3','h4','h5','h6'])
    markdown = ["## Contents\n"]
    for h in headings:
        level = int(h.name[1])
        prefix = "#" * level
        title = h.get_text(strip=True)
        markdown.append(f"{prefix} {title}")
    return {"outline": "\n\n".join(markdown)}

