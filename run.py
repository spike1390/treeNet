from flask import Flask, render_template
from views.home import index
from views.network import network
from models import path
import os
app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'test.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.register_blueprint(index, url_prefix='/home')
app.register_blueprint(network, url_prefix='/network')
@app.route('/')
def hello_world():

    path =  app.config['DATABASE']
    return render_template('login.html')


if __name__ == '__main__':
    app.run()