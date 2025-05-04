from pathlib import Path
from typing import Self

import lancedb
import polars as pl
from agents import function_tool
from lancedb.embeddings import get_registry
from lancedb.embeddings.openai import OpenAIEmbeddings
from lancedb.pydantic import LanceModel, Vector
from pydantic import BaseModel

func: OpenAIEmbeddings = (
    get_registry().get("openai").create(name="text-embedding-ada-002")
)


class Transcription(LanceModel):
    title: str
    published: str
    video_id: str
    channel_id: str
    url: str
    id: str
    text: str = func.SourceField()
    start: float
    end: float
    vector: Vector(func.ndims()) = func.VectorField()  # type: ignore


db_path = Path("./data/db")
db_path.parent.mkdir(parents=True, exist_ok=True)


async def prepare_data(connection: lancedb.AsyncConnection):
    connection = await lancedb.connect_async(db_path)
    df = pl.read_ndjson("youtube-transcriptions_sample.jsonl")
    table = await connection.create_table(
        "transcriptions", schema=Transcription, mode="overwrite"
    )
    await table.add(df)


async def query_sample(table: lancedb.Table):
    query = "What is RAG?"
    query = await table.search(query)


class TranscriptionForAI(BaseModel):
    title: str
    text: str
    published: str

    @classmethod
    def from_transcription(cls, transcription: Transcription) -> Self:
        return cls(
            title=transcription.title,
            text=transcription.text,
            published=transcription.published,
        )


# From lancedb tutorial https://github.com/lancedb/vectordb-recipes/tree/main/examples/Youtube-Search-QA-Bot


@function_tool
async def transcription_search(
    query: str, n: int, pre_filter: str | None = None, post_filter: str | None = None
) -> Transcription:
    """Search for transcriptions in the LanceDB."""
    search_result = table.search(query).limit(n).to_pydantic(Transcription)

    return search_result


print(search_result)
