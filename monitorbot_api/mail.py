import os
from flask import Flask
from flask_mail import Mail



app = Flask(__name__)


app.config['MAIL_SERVER']='smpt.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('Mail_USERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('Mail_PASSWORD')
app.config['DEFAULT_MAIL_SUBJECT']='[MonitorBot Check Report]'
app.config['DEFAULT_MAIL_SUBJECT']='MonitorBot <monitorbot.app@gmail.com>'
app.config['SECRET_KEY']='random_string'
app.config['DEFAULT_ADMIN']='MonitorBot <monitorbot.app@gmail.com>'


mail = Mail(app)

if __name__ == '__main__':
 app.run(debug=True)



from flask.ext.mail import Message

@app.route("/")
def index():

    msg = Message("Hello, Welcome to MonitorBot",
                  sender="monitorbot.app@gmail.com",
                  recipients=["inioluwafageyinbo@gmail.com"])

