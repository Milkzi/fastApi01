import uvicorn
from apps import create_app


app = create_app()

if __name__ == '__main__':
    uvicorn.run(app="main:app",
                host='127.0.0.1',
                port=9000,
                debug=True,
                workers=1,
                reload=True)
