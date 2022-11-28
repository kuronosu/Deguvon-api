import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from bson import ObjectId
from pymongo import MongoClient
from typing import Optional, Union

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URL"))
db = client.deguvon

app = FastAPI()

class Response404(BaseModel):
    detail: str = Field(..., example="Item not found")

response404 = {404: {"model": Response404, "description": "The item was not found"}}
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


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
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

# @app.get("/animes", response_model=list[Anime])
# def anime_list() -> list[Anime]:
#     return animes_list

@app.get("/animes/{flvid}", response_model=Anime, responses={**response404})
def anime_detail(flvid: int) -> Anime:
    if (student := db.animes.find_one({"flvid": flvid})) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Anime {flvid} not found")
