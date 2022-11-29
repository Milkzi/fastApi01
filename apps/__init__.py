from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .index.indexpage import index_app
from .websockets.websockets_view import websocket_endpoint
from fastapi.middleware.wsgi import WSGIMiddleware

from starlette.staticfiles import StaticFiles
from apps.flask import create_flask_app
flask_app = create_flask_app()
def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        # 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
        allow_origins=["*"],
        # 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
        allow_credentials=False,
        # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
        allow_methods=["*"],
        # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
        # 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
        allow_headers=["*"],
        # 可以被浏览器访问的响应头, 默认是 []，一般很少指定
        # expose_headers=["*"]
        # 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
        # max_age=1000
    )

    app.mount("/static", app=StaticFiles(directory='static'), name='static')
    app.include_router(index_app)
    app.add_api_websocket_route(path='/ws/{client_id}', endpoint=websocket_endpoint)
    app.mount("/flask", WSGIMiddleware(flask_app))

    return app
