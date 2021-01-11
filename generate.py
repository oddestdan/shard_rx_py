import requests
from faker import Faker
from app.internal.schemas import study as study_schema

faker = Faker()

HOST = 'http://127.0.0.1:8000'

data = [study_schema.Student(
    name = faker.name(),
    phone_number = faker.phone_number(),
    address = faker.address(),
    mail = faker.email(),
    sex = faker.simple_profile()['sex']
  ).dict() for _ in range(50)
]

result = requests.post(HOST + "/batch/students/", json=data)

print("Status:", result.status_code, '\n', "Response:", result.json())
