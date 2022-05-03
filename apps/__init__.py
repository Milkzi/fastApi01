from fastapi import FastAPI
from .index.indexpage import index_app
from .websockets.websockets_view import websocket_endpoint
from starlette.staticfiles import StaticFiles


def create_app():
    app = FastAPI()
    app.mount("/static", app=StaticFiles(directory='static'), name='static')
    app.include_router(index_app)
    app.add_api_websocket_route(path='/ws/{client_id}', endpoint=websocket_endpoint)

    return app
