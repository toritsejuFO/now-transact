import os
import logging
from dotenv import load_dotenv
from connexion.resolver import RestyResolver
from flask_migrate import Migrate

load_dotenv()

from app import create_app, db
from app.exceptions import setup_error_handler

connexion_app = create_app()
connexion_app.add_api('../api_spec.yml', resolver=RestyResolver('app.controllers'))
app = connexion_app.app

logging.getLogger(os.getenv('APP_NAME')).setLevel(logging.INFO)

Migrate(app, db)
setup_error_handler(app)

@app.route('/')
def home():
    return 'Welcome to Now Transact', 200

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
