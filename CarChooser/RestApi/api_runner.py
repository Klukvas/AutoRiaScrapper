from .app import create_app


def runserver():
    app = create_app()
    app.run()


if __name__ == '__main__':
    runserver()
