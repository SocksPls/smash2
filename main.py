import datetime, random, json, pymongo
from flask import Flask, render_template, Markup, request, abort, session, g
import db as dblib
#from smash import app, conf

app = Flask(__name__)

#Connect to and define db
connection = pymongo.MongoClient()
db = connection.testdb
qdb = db.quotes

def timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S %d/%m/%y")

def message(level, msg):
    return render_template(
        "message.html",
        alertclass=level,
        message=msg,
        title="Message"
    )

@app.route('/')
def index():
    news = "No quotes yet!"
    #welcome = conf.config['MOTD']
    welcome = "MOTD"
    print(qdb.find().count())
    qCount = qdb.find({"hidden": False}).count()
    print(type(qCount))
    news = "Home of " + str(qCount) + " dumb quotes!"
    if qCount > 0:
        rand_quote = dblib.get_random_quote()
        quote_text = Markup.escape(rand_quote['quote'])#.replace('\n', '<br />')
        news = quote_text
        permalink = str(rand_quote['id'])

    return render_template(
        "index.html",
        title="Quotes",
        welcometext=welcome,
        newstext=news,
        permalink=permalink
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
