#!flask/bin/python
from app import create_app

app = create_app('DEVELOPMENT')
app.run(host='0.0.0.0')
