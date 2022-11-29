from apps.flask.model import db
from apps.flask import create_flask_app
from flask_migrate import Migrate

app = create_flask_app()

Migrate(app=app, db=db)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, reload=True)
