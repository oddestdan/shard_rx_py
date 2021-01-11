from fastapi import FastAPI
from .config.db import database
from .schemas import study as study_schema
from .models.study import students

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.post("/students/")
async def create_student(student: study_schema.Student):
    query = students.insert().values(
        name = student.name,
        phone_number = student.phone_number,
        address = student.address,
        mail = student.mail,
        sex = student.sex
    )
    created_id = await database.execute(query)
    return {
        **student.dict(),
        "id": created_id
    }

@app.get("/students/", response_model = study_schema.StudentGroup)
async def get_students_group(skip: int = 0, limit: int = 100):
    students_query = students.select().offset(skip).limit(limit)
    count_query = students.select().count()

    db_students = await database.fetch_all(students_query)
    count = await database.fetch_val(count_query)

    return study_schema.StudentGroup(
        count = count,
        limit = limit,
        offset = skip,
        data = db_students
    )

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
