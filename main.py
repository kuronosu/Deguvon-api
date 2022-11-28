import json
from fastapi import FastAPI
from pydantic import BaseModel

class Genre(BaseModel):
    url: str
    name: str

class Episode(BaseModel):
    flvid: int
    number: int | float

class Anime(BaseModel):
    flvid: int
    slug: str
    banner: str
    cover: str
    status: str
    synopsis: str
    title: str
    type: str
    votes: int
    followers: int
    score: float
    episodes: list[Episode]
    genres: list[Genre]

animes: dict[str, Anime] = {key: Anime.parse_obj(val) for key, val in json.load(open('animes.json', encoding='utf-8')).items()}
animes_list: list[Anime] = list(animes.values())

app = FastAPI()

@app.get("/animes", response_model=list[Anime])
def anime_list() -> list[Anime]:
    return animes_list

@app.get("/animes/{flvid}", response_model=Anime)
def anime_detail(flvid: int) -> Anime:
    return animes.get(f'{flvid}')
