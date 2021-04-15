from pymongo import MongoClient
from pymongo.cursor import CursorType


if __name__=="__main__":
    host = "localhost"
    port = "27017"
    conn = MongoClient(host, int(port))
    print(conn)
    db = conn.get_database("testdb")
    print(db)
    print(db.collection_names())

    results = db.testdb.find({})
    for r in results:
        print(r)

    results = db.testdb.insert_many([{'x': i} for i in range(2)])
    for result in results.inserted_ids:
        print(result)