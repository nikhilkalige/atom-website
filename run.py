#!flask/bin/python
from app import create_app

app = create_app('DEVELOPMENT')


if __name__ == "__main__":
    app.run()
