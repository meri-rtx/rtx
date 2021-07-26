from elasticsearch import Elasticsearch
import gzip
import json
import pandas as pd

es = Elasticsearch(hosts="localhost", port=9200)  # 객체 생성


def searchAPI(index_name):
    es = Elasticsearch()
    index = index_name
    body = {
        'size':10000,
        'query':{
            'match_all':{}
        }
    }
    res1 = es.search(index=index, body=body)
    res = json.dumps(res1, ensure_ascii=False, indent=4)
    return res


def parse(path: str):
    g = gzip.open(path, "rb")
    for l in g:
        yield eval(l)


def parse_json_to_df(path: str) -> pd.DataFrame:
    i = 0
    df_dict = {}
    for d in parse(path):
        df_dict[i] = d
        i += 1
        if i % 100000 == 0:
             print("Rows processed: {:,}".format(i))

    df = pd.DataFrame.from_dict(df_dict, orient="index")
    df["_index"] = df["_index"].astype(str)
    df["_id"] = df["_id"].astype(str)
    # df["택지면적"] = df["택지면적"].astype(str)
    return df


result = searchAPI('redevelopment')
result2 = json.dumps(result, ensure_ascii=False, indent=4)
aaa = parse_json_to_df(result2)

