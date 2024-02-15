# run.py
from application import create_app, db
from application.model import models
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5102)