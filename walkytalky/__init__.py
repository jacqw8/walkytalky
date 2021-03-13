from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a372e6655ca049a0a1b2b0fd0356ec69'

from walkytalky import routes