import logging
import os
import sys
# from dotenv import load_dotenv

from flask import (
    Flask,
    jsonify,
    render_template,
    request
)
from logger import log
from db import DB
from sender import send_mail

# load_dotenv('/home/azureuser/Ansible/.env')
mydb = DB()



logging.basicConfig(filename="LOG.log",
                    filemode="a",
                    format='%(asctime)s: %(levelname)s: %(message)s',
                    level=logging.DEBUG,
                    datefmt='[%Y-%m-%d %H:%M:%S]')


app = Flask(__name__)



@app.route("/", methods=['GET'])
@log
def index():
    # DB.set_table()
    return render_template('index.html')

#------------- init flask .py------------

@app.route('/id', methods=['GET', 'POST'])
@app.route('/id/<name>', methods=['GET', 'POST'])
@log
def id(name='undefine'):
    r = request.form
    user = r['user']
    mail = r['mail']
    with DB() as mydb:
        checking = mydb.insert_user(user) 
        max_users = mydb.get_max().strip(",()")
    if not user or not mail:
        return render_template('index.html') 
    elif checking == False:
        return render_template('index.html', checking=False)
    else:
        # with DB() as mydb:
            # mydb.insert_user(user)        
            # max_users = mydb.get_max().strip(",()")
        # mailing(mail, jsonify(mydb.get_users()))
        send_mail(mail)
        return render_template('id.html', name=user, max_users=max_users) 

@app.route('/json', methods=['GET'])
@log
def results():
    with DB() as mydb:
        resp = jsonify(mydb.get_users())
    return resp

# @app.route("/inc", methods=['GET'])
# @log
# def inc():
#     mydb.insert_user(name)



@app.errorhandler(404)
@log
def page_not_found(error):
    return 'This page does not exist', 404

@app.errorhandler(500)
@log
def special_exception_handler(error):
    return 'Database connection failed', 500

@app.route('/hello/<name>')
@log
def hello(name):
    return 'Hello {} !'.format(name.capitalize())


if __name__ == '__main__':
    with DB() as mydb:
        # mydb.del_table()
        # mydb.set_table()
        # mydb.test_insert()
        app.run(host='52.148.138.186', port=3000, debug=True)
        # os.environ['FLASK_RUN_PORT']