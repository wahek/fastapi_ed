import logging
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Body
from pydantic import BaseModel, Field

"""
Создать API для добавления нового пользователя в базу данных. Приложение
должно иметь возможность принимать POST запросы с данными нового
пользователя и сохранять их в базу данных.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей.
Создайте маршрут для добавления нового пользователя (метод POST).
Реализуйте валидацию данных запроса и ответа.
"""


class UserGet(BaseModel):
    user_id: int = ...
    name: str = Field(default='Standard user', max_length=20, title='Input username')
    email: str = ...


class UserPost(UserGet):
    password: str = ...


db: list[UserPost] = []

app = FastAPI()


@app.get('/users/{user_id}', response_model=UserGet)
def user_get(user_id: Annotated[int, Path(title="The ID of the user to get")]) -> UserGet:
    for user in db:
        if user.user_id == user_id:
            return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.post('/users')
def user_post(user: UserPost) -> str:
    for u in db:
        if u.user_id == user.user_id:
            raise HTTPException(status_code=401, detail='There is already a user with this id')
    db.append(user)
    return 'append valid'


@app.put('/users/{user_id}')
def user_put(user: UserPost, pswd: str) -> str:
    for i, u in enumerate(db):
        if u.user_id == user.user_id:
            if u.password == pswd:
                db[i] = user
                return 'User update'
            raise HTTPException(status_code=402, detail='permission deni, invalid password')
    raise HTTPException(status_code=401, detail='User not found')


@app.delete('/users/{user_id}')
def user_del(user_id, pswd: str) -> str:
    for i, u in enumerate(db):
        if u.user_id == user_id:
            if u.password == pswd:
                db.pop(i)
                return 'User delete'
            raise HTTPException(status_code=402, detail='permission deni, invalid password')
    raise HTTPException(status_code=401, detail='User not found')
