from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Union
from deta import Deta


load_dotenv()

deta = Deta()

db_animes = deta.Base("Animes")

app = FastAPI()


class Response404(BaseModel):
    detail: str = Field(..., example="Item not found")


response404 = {404: {"model": Response404,
                     "description": "The item was not found"}}


class Genre(BaseModel):
    url: str
    name: str


class Episode(BaseModel):
    flvid: int
    number: Union[int, float]


class Anime(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
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
    genres: list[str]
    url: str
    next_episode: Union[str, None] = None
    # related: list[Related]
    # key: str = Field(..., alias="_key")
# @app.get("/animes", response_model=list[Anime])
# def anime_list() -> list[Anime]:
#     return animes_list


@app.get("/animes/{slug}", response_model=Anime, responses={**response404})
def anime_detail(slug: str) -> Anime:
    anime: Union[dict, None] = db_animes.get(slug)  # type: ignore
    if anime is None:
        raise HTTPException(
            status_code=404, detail=f"Anime '{slug}' not found")
    return Anime.parse_obj(anime)
