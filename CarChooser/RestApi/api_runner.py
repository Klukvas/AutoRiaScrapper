from .app import create_app


def runserver():
    app = create_app('development')
    app.run(port=5001, host="0.0.0.0")


if __name__ == '__main__':
    runserver()
