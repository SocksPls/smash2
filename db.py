import pymongo, nanoid
from config import config

connection = pymongo.MongoClient(config["db"]["server"])
db = connection[config["db"]["database"]]
qdb = db[config["db"]["collection"]]

count_live_quotes = lambda: qdb.find({"hidden": False, "approved": True}).count()
quote_live = lambda quote_id: bool(qdb.find_one({"hidden": False, "approved": True}))
tag_live = lambda tag: bool(
    qdb.find_one({"hidden": False, "approved": True, "tags": tag})
)


def get_random_quote():

    # TODO: there might be a better way to get a random document
    x = list(
        qdb.aggregate(
            [{"$match": {"hidden": False, "approved": True}}, {"$sample": {"size": 1}}]
        )
    )[0]

    return x if x else False


def get_quote_by_id(quote_id):
    if quote_live(quote_id):
        return qdb.find_one({"id": quote_id})
    else:
        return False


def add_quote(quote, tags, author):
    quote_id = nanoid.generate(size=config["quote-id-length"])
    qdb.insert_one(
        {
            "id": quote_id,
            "quote": quote,
            "tags": tags,
            "author": author,
            "hidden": False,
            "approved": False,
        }
    )
    return quote_id


def get_latest_quotes(page=1):
    return list(
        qdb.find({"hidden": False, "approved": True})
        .sort("_id", -1)
        .limit(page * 10)[(page - 1) * 10 :]
    )


def get_live_quotes_by_tag(tag):
    return list(
        qdb.find({"hidden": False, "approved": True, "tags": tag}).sort("_id", 1)
    )


def get_all_tags():
    return qdb.find({"hidden": False, "approved": True}).distinct("tags")


def count_live_quotes_by_tag():
    quotes = {}
    for tag in get_all_tags():
        quotes[tag] = len(get_live_quotes_by_tag(tag))
    return quotes
