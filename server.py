#!/usr/bin/env python3
import yt_dlp
import json

from fastapi import FastAPI
from pydantic import BaseModel

url = "https://www.youtube.com/watch?v=H2r25lVcIHw"

options = {
    "quiet": True,
    "geo_bypass": True,
    # "format": "bv[ext=webm]+ba[ext=webm]/bv[ext=mp4]+ba[ext=mp4]/bv+ba",
    "format": "bv+ba",
}

app = FastAPI()

class StreamModel(BaseModel):
    format_id: str
    url: str
    ext: str
    codec: str

class InfoModel(BaseModel):
    id: str
    title: str | None
    description: str | None
    channel_id: str
    channel_url: str
    duration: int
    tags: list[str]

    video: StreamModel
    audio: StreamModel


@app.get("/youtube/info/{vid}")
def info(vid: str):
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)

        video_info: dict = next(f for f in info["requested_formats"] if f["vcodec"] != "none")
        audio_info: dict = next(f for f in info["requested_formats"] if f["acodec"] != "none")

        return InfoModel(
            id          = vid,
            title       = info.get("title"),
            description = info.get("description"),
            channel_id  = info["channel_id"],
            channel_url = info["channel_url"],
            duration    = info["duration"],
            tags        = info["tags"],

            video = StreamModel(
                format_id = video_info["format_id"],
                url       = video_info["url"],
                ext       = video_info["ext"],
                codec     = video_info["vcodec"]
            ),

            audio = StreamModel(
                format_id = audio_info["format_id"],
                url       = audio_info["url"],
                ext       = audio_info["ext"],
                codec     = audio_info["acodec"]
            )
        )
