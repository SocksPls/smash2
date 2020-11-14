import pymongo
connection = pymongo.MongoClient()
db = connection.smash
qdb = db.quotes
adb = db.accounts

def get_random_quote():
    x = dict( qdb.aggregate([
        { "$match": { "hidden": False } },
        { "$sample": { "size": 1 } }
    ]) )
    print(x)
    return(x)


def add_quote(quote, tags, author):
    qdb.insert_one({
        "quote": quote,
        "tags": tags,
        "author": author
    })
