from flask import Flask, render_template, request, jsonify
from views.home import index
from views.network import network
from views.message import message
from models import path, mydb
import os, random, threading, time, json
app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'test.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    RANDOMSEED=0
))
path.db_path = app.config['DATABASE']
app.register_blueprint(index, url_prefix='/home')
app.register_blueprint(network, url_prefix='/network')
app.register_blueprint(message,url_prefix='/message')
Delay = 5

@app.route('/')
def hello_world():
    path.db_path = app.config['DATABASE']
    return render_template('login.html')

@app.route("/data", methods=['GET'])
def data():
    """Primary data source for AJAX/REST queries. Get's the server's current
    time two ways: as raw data, and as a formatted string. NB While other
    Python JSON emitters will directly encode arrays and other data types,
    Flask.jsonify() appears to require a dict. """
    re = json.dumps(find_all_inactiveNode())
    return jsonify(result1 = re)

@app.route("/updated")
def updated():
    """Wait until something has changed, and report it. Python has *meh* support
    for threading, as witnessed by the umpteen solutions to this problem (e.g.
    Twisted, gevent, Stackless Python, etc). Here we use a simple check-sleep
    loop to wait for an update. app.config is handy place to stow global app
    data."""
    while not app.config['updated']:
        time.sleep(3)
    app.config['updated'] = False  # it'll be reported by return, so turn off signal
    return "changed!"


@app.route("/changeRand")
def changeRand():
    a = request.args.get('a', 0, type=str)
    app.config['RANDOMSEED'] = int(a)
    return jsonify()

@app.route("/randomSpeed")
def randomSpeed():
    return jsonify(result1 = app.config['RANDOMSEED'])


@app.route("/")
def main():
    return render_template("index.html")


def update():
    randomly_inactive_node(app.config['RANDOMSEED'])
    global t
    t = threading.Timer(Delay, update)
    t.start()

def randomly_inactive_node(seed):
    num=random.randint(0,100)
    if(num<seed):
        mydb.open()
    # active =1 means it is active
        result = mydb.query_db('select * from node WHERE active=1', one=False)
        mydb.close_db()
        nidList=[]
        if result:
            for nid in result:
                nidList.append(nid['nid'])
            inactive_nid=nidList[random.randint(0, len(nidList)-1)]
        # set not whose nid is inactive_nid to inactive status, pass nid and inactive(0)
            change_node_status(inactive_nid, 0)
            app.config['updated'] = True
            print find_all_inactiveNode()

# get all inactive node nid
def find_all_inactiveNode():
    mydb.open()
    # active =1 means it is active
    result = mydb.query_db('select * from node WHERE active=0', one=False)
    mydb.close_db()
    nidList=[]
    if result:
        for nid in result:
            nidList.append(nid['nid'])
    return nidList

# active a inactive node. input must be a inactive node's nid
def change_node_status(nid, active):
    mydb.open()
    # active =1 means it is active
    result = mydb.insert_db('update node SET active=?  WHERE nid=?',[active,nid])
    mydb.close_db()


if __name__ == '__main__':
    app.config['updated'] = False
    t = threading.Timer(Delay, update)
    t.start()
    app.run(threaded= True,host='0.0.0.0',use_reloader=False)