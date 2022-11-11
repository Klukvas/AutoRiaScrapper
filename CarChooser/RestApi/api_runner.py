from .app import create_app
import os

def runserver():
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(port=5001, host="0.0.0.0")


if __name__ == '__main__':
    runserver()
