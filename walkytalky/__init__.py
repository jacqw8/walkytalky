from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f5a0b8e461a73a4a6fbd4aab758b4b0a'

from walkytalky import routes