import datetime, random, json, pymongo
from flask import Flask, render_template, Markup, request, abort, session, g
import db
from config import config

app = Flask(__name__)
app.secret_key = config["secret-key"]


timestamp = lambda: datetime.datetime.now().strftime("%H:%M:%S %d/%m/%y")


@app.context_processor
def inject_config():
    return {"site_name": config["site-name"]}


@app.route("/")
def index():
    news = "No quotes yet!"
    welcome = config["MOTD"]
    quotes_count = db.count_live_quotes()

    if (quotes_count > 0) and (config["random-quote"]):
        random_quote = db.get_random_quote()
        news = Markup.escape(random_quote["quote"])
        permalink = str(random_quote["id"])
    elif quotes_count > 0:
        news = "Home of " + str(quotes_count) + " quotes!"
        permalink = None
    else:
        news = "There are no quotes in the database!"
        permalink = None

    return render_template(
        "index.html",
        title="Quotes",
        header=welcome,
        newstext=news,
        permalink=permalink,
    )


@app.route("/latest")
def latest():
    return render_template(
        "list.html",
        title="Latest",
        header="Latest Quotes",
        latest=True,
        quotes=db.get_latest_quotes(),
    )


@app.route("/tags")
def tags():
    return render_template(
        "tags.html", title="Tags", tags=db.count_live_quotes_by_tag()
    )


@app.route("/tags/<t>")
def tag(t):
    if db.tag_live(t):
        return render_template(
            "list.html",
            title=t,
            header="Quotes matching: " + t,
            quotes=db.get_live_quotes_by_tag(t),
        )
    else:
        return render_template(
            "message.html",
            title="Error!",
            message={
                "type": "danger",
                "heading": "No matching quotes",
                "message": f'There are no quotes with the tag "{t}" in the database',
            },
        )


@app.route("/quote/<quote_id>")
def quote(quote_id):
    return render_template(
        "quote.html", title="Quote " + quote_id, quote=db.get_quote_by_id(quote_id)
    )


@app.route("/new", methods=["GET", "POST"])
def new_quote():
    if request.method == "GET":
        return render_template(
            "new.html",
            title="New Quote",
        )
    elif request.method == "POST":
        author = request.form["author"]
        quote = request.form["quote"]
        tags_list = [i.strip() for i in request.form["tags"].split(",")]
        db.add_quote(quote, tags_list, author)
        return render_template(
            "message.html",
            message={
                "type": "success",
                "heading": "Thanks for being awesome!",
                "message": "Your quote is currently awaiting approval from a site administrator",
            },
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
