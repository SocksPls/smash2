import datetime, random, json, pymongo
from flask import Flask, render_template, Markup, request, abort, session, g
import db
#from smash import app, conf

app = Flask(__name__)

#Connect to and define db
connection = pymongo.MongoClient()
real_db = connection.testdb
qdb = real_db.quotes

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
    #print(qdb.find().count())
    qCount = qdb.find({"hidden": False}).count()
    #print(type(qCount))
    news = "Home of " + "5" + " dumb quotes!"
    if qCount > 0:
        rand_quote = db.get_random_quote()
        quote_text = Markup.escape(rand_quote['quote']) if rand_quote else "There are no quotes in the database!"
        news = quote_text
        permalink = str(rand_quote['id'])

    return render_template(
        "index.html",
        title="Quotes",
        welcometext=welcome,
        newstext=news,
        permalink=permalink
    )

@app.route('/latest')
def latest():
    return render_template(
        "list.html",
        title="Latest",
        header="Latest Quotes",
        quotes=db.get_latest_quotes()
    )


@app.route('/tags')
def tags():
    return render_template(
        "tags.html",
        title="Tags",
        tags=db.count_live_quotes_by_tag()
    )

@app.route('/tags/<t>')
def tag(t):
    if db.tag_live(t):
        return render_template(
            "list.html",
            title=t,
            header="Quotes matching: " + t,
            quotes=db.get_live_quotes_by_tag(t)
        )
    else:
        return render_template(
            "message.html",
            title="Error!",
            message={
                "type": "danger",
                "heading": "No matching quotes",
                "message": f"There are no quotes with the tag \"{t}\" in the database"
            }
        )


@app.route('/quote/<quote_id>')
def quote(quote_id):
    return render_template(
        "quote.html",
        title="Quote " + quote_id,
        quote= db.get_quote_by_id(quote_id)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
