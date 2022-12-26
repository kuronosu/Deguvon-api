from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Union
from deta import Deta


load_dotenv('.env')

deta = Deta()

animes = deta.Base("animes")

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

    class Config:
        arbitrary_types_allowed = True
        # json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

# @app.get("/animes", response_model=list[Anime])
# def anime_list() -> list[Anime]:
#     return animes_list


@app.get("/animes/{flvid}", response_model=Anime, responses={**response404})
def anime_detail(flvid: int) -> Anime:
    res = animes.fetch({"flvid": flvid})
    if res.count == 0:
        raise HTTPException(status_code=404, detail=f"Anime {flvid} not found")
    return res.items[0]
