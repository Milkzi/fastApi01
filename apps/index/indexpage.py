from fastapi import APIRouter
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
import json
import uuid

tmp = Jinja2Templates(directory='templates')
index_app = APIRouter()


@index_app.get("/")
async def root():
    return {"message": "Hello World"}


@index_app.get("/hello")
async def ws_hello(request: Request):
    uid = uuid.uuid4()
    print(uid)
    with open('static/file/city.json', 'r', encoding='utf-8') as f:
        city = json.load(f)
    city = json.dumps(city, ensure_ascii=False)

    return tmp.TemplateResponse('index.html', {'request': request, 'uid': uid, 'cities': city})
