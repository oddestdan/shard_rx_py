import requests
import rx
from typing import List
from fastapi import FastAPI
from rx import operators
from .schemas import study as study_schema
from .services import retrieve_all_students
from .config.shard import shard_config

app = FastAPI()

@app.post("/batch/students/")
def create_students(students: List[study_schema.Student]):
    stream = rx.from_list(students).pipe(
        operators.map(lambda student: (student, shard_config["shard_rules"]['students'](student)))
    )

    stream.subscribe(
        on_next = lambda i: requests.post(
            shard_config['shard_servers'][i[1]]['address'] + "/students/", json=i[0].dict()
        ),
        on_error = None,
        on_completed = None
    )

@app.get("/batch/students/", response_model=List[study_schema.Student])
def retrieve_students():
    return retrieve_all_students()
