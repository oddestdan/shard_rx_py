import asyncio
from typing import List
import requests
import rx
from rx.subject import Subject
from .schemas import study as study_schema
from .config.shard import shard_config

async def fetch_pages(observer: Subject, i: int, uri: str, page_size: int):
    result = requests.get(uri + f"?offset={i * page_size}&limit={page_size}")
    payload = study_schema.StudentGroup(**result.json())

    for student in payload.data: observer.on_next(student)

async def fetch_from_shard(observer: Subject, uri: str, page_size: int):
    result = requests.get(uri + f"?offset=0&limit={page_size}")
    payload = study_schema.StudentGroup(**result.json())

    for student in payload.data: observer.on_next(student)
    await asyncio.gather(*[fetch_pages(observer, i, uri, page_size) for i in range(1, payload.count // page_size)])



def fetch_all_students(observer: Subject, scheduler):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []

    for server in shard_config['shard_servers'].values():
        tasks.append(fetch_from_shard(observer, server['address'] + "/students/", 10))
    loop.run_until_complete(asyncio.gather(*tasks))
    observer.on_completed()

def retrieve_all_students() -> List[study_schema.Student]:
    stream = rx.create(fetch_all_students)
    result = []

    stream.subscribe(
        on_next=lambda i: result.append(i),
        on_error=None,
        on_completed=None
    )

    return result
