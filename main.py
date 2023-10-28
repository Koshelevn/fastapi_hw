from enum import Enum
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing_extensions import Literal

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return "Success"


@app.post('/post')
def post_post():
    new_timestamp = Timestamp(id=post_db[-1].id + 1, timestamp=int(datetime.now().timestamp()))
    post_db.append(new_timestamp)
    return new_timestamp


@app.get('/dog')
def get_dogs(kind: str = Literal[DogType.bulldog, DogType.dalmatian, DogType.terrier]):
    if kind not in [DogType.bulldog, DogType.dalmatian, DogType.terrier]:
        raise HTTPException(status_code=422, detail='"kind" field should be one of '
                                                    f'{DogType.bulldog.value, DogType.dalmatian.value, DogType.terrier.value}')
    dogs = dict(filter(lambda x: x[1].kind == kind, dogs_db.items())).values()
    return list(dogs)


@app.post('/dog')
def post_dog(name: str, pk: int, kind: str):
    if pk in dogs_db.keys():
        raise HTTPException(status_code=409, detail='The specified PK already exists.')
    if kind not in [DogType.bulldog, DogType.dalmatian, DogType.terrier]:
        raise HTTPException(status_code=422, detail='"kind" field should be one of '
                                                    f'{DogType.bulldog.value, DogType.dalmatian.value, DogType.terrier.value}')
    if not name:
        raise HTTPException(status_code=422, detail='"Name" field should not be empty')
    new_dog = Dog(name=name, pk=pk, kind=DogType(kind))
    dogs_db[new_dog.pk] = new_dog
    return new_dog


@app.get('/dog/{pk}')
def get_dog_pk(pk: int):
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=409, detail='The specified PK are not present in DB')
    return dogs_db[pk]


@app.patch('/dog/{pk}')
def get_dog_pk(pk: int, name: str, kind: str):
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=409, detail='The specified PK is not present in DB')
    if not name:
        raise HTTPException(status_code=422, detail='"Name" field should not be empty')
    if kind not in [DogType.bulldog, DogType.dalmatian, DogType.terrier]:
        raise HTTPException(status_code=422, detail='"kind" field should be one of '
                                                    f'{DogType.bulldog.value, DogType.dalmatian.value, DogType.terrier.value}')
    dogs_db[pk] = Dog(name=name, pk=pk, kind=DogType(kind))
    return dogs_db[pk]
