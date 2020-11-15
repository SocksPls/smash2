import pymongo, nanoid
connection = pymongo.MongoClient()
db = connection.smash
qdb = db.quotes
adb = db.accounts

live_quotes_count = lambda: qdb.find({ "hidden": False, "approved": True })

def get_random_quote():

    #TODO: there might be a better way to get a random document
    x = list(qdb.aggregate([
        { "$match": { "hidden": False, "approved": True } },
        { "$sample": { "size": 1 } }
    ]))[0]

    return(x if x else False)


def add_quote(quote, tags, author):
    qdb.insert_one({
        "id": nanoid.generate(size=12),
        "quote": quote,
        "tags": tags,
        "author": author,
        "hidden": False,
        "approved": False
    })


def get_latest_quotes(page=1):
    return list(qdb \
        .find({ "hidden": False, "approved": True }) \
        .sort( "_id", 1 ) \
        .limit(page*10)[(page-1)*10:])
