from sqlalchemy import Column, Integer, String, MetaData, Table

from ..config.db import engine


metadata = MetaData()

students = Table(
    "students",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', String),
    Column('phone_number', String),
    Column('address', String),
    Column('mail', String),
    Column('sex', String)
)

metadata.create_all(engine)

