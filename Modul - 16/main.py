# Импорт библиотек
from fastapi import FastAPI, Path, status, Body, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel


# Инициализация приложения
app = FastAPI()
# База данных сообщений
messages_db = []
# Подключение шаблонизатора
templates = Jinja2Templates(directory='templates')



class Message(BaseModel):
    id: int = None
    text: str


# Получение всех сообщений
@app.get('/')
async def get_all_messages(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('message.html', {'request': request, 'messages': messages_db})


# Получение сообщения по ID
@app.get('/message/{message_id}')
async def get_message(request: Request, message_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse('message.html', {'request': request, 'message': messages_db[message_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail='Message not found!')


# Создание нового сообщения
@app.post('/message',  status_code=status.HTTP_201_CREATED)
async def create_message(request: Request, message: str = Form()) -> HTMLResponse:
    if messages_db:
        message_id = max(messages_db, key=lambda m: m.id).id + 1
    else:
        message_id = 0
    messages_db.append(Message(id=message_id, text=message))
    return templates.TemplateResponse('message.html', {'request': request, 'messages': messages_db})


# Обновление сообщения
@app.put('/message/{message_id}')
async def update_message(message_id: int, message: str = Body()) -> str:
    try:
        edit_message = messages_db[message_id]
        edit_message.text = message
        return 'Message is updated!'
    except IndexError:
        raise HTTPException(status_code=404, detail='Message not found!')

# Удаление сообщения по ID
@app.delete('/message/{message_id}')
async def kill_message(message_id: int) -> str:
    try:
        messages_db.pop(message_id)
        return f'Message with ID {message_id} is deleted!'
    except IndexError:
        raise HTTPException(status_code=404, detail='Message not found!')


# Удаление всех сообщений
@app.delete('/')
async def kill_all_messages() -> str:
    messages_db.clear()
    return 'All messages is deleted!'
