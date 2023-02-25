import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app

app = create_app(os.getenv('ENV', 'development'))

@app.route('/')
def home():
    return 'Welcome to Now Transact', 200

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=app.config['PORT'] or 3003,
        debug=app.config['FLASK_DEBUG'] or True
    )
