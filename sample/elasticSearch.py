from elasticsearch import Elasticsearch
import pprint as ppr
import json
import pandas as pd

class ElaAPI:
    es = Elasticsearch(hosts="localhost", port=9200)   # 객체 생성
    @classmethod
    def srvHealthCheck(cls):
        health = cls.es.cluster.health()
        print (health)

    @classmethod
    def allIndex(cls):
        # Elasticsearch에 있는 모든 Index 조회
        print (cls.es.cat.indices())

    # @classmethod
    # def dataInsert(cls):
    #     # ===============
    #     # 데이터 삽입
    #     # ===============
    #     with open("../json_doc_make/tst.json", "r", encoding="utf-8") as fjson:
    #         data = json.loads(fjson.read())
    #         for n, i in enumerate(data):
    #             doc = {"cont"   :i['cont'],
    #                    "mnagnnm":i["mnagnnm"],
    #                    "post"   :i["post"],
    #                    "rgdt"   :i["rgdt"],
    #                    "rgter"  :i["rgter"],
    #                    "tel"    :i["tel"],
    #                    "title"  :i["title"]}
    #             res = cls.es.index(index="today19020301", doc_type="today", id=n+1, body=doc)
    #             print (res)
    #
    @classmethod
    def searchAll(cls, indx=None):
        # ===============
        # 데이터 조회 [전체]
        # ===============
        res = cls.es.search(
            index = "redevelopment",  #, doc_type = "today",
            body = {
                "query":{"match_all":{}}
            }
        )
        print(json.dumps(res, ensure_ascii=False, indent=4))

    # def parse_json_to_df(path: str) -> pd.DataFrame:
    #     i = 0
    #     df_dict = {}
    #     for d in parse(path):
    #         df_dict[i] = d
    #         i += 1
    #         if i % 100000 == 0:
    #             print("Rows processed: {:,}".format(i))
    #
    #     df = pd.DataFrame.from_dict(df_dict, orient="index")
    #     df["건폐율"] = df["건폐율"].astype(str)
    #     df["지하층수"] = df["지하층수"].astype(str)
    #     df["택지면적"] = df["택지면적"].astype(str)
    #     return df
    #
    # parse_json_to_df(searchAll())

    # @classmethod
    # def searchFilter(cls):
    #     # ===============
    #     # 데이터 조회 []
    #     # ===============
    #     res = cls.es.search(
    #         index = "today19020301", doc_type = "today",
    #         body = {
    #             "query": {"match":{"post":"산림교육문화과"}}
    #         }
    #     )
    #     ppr.pprint(res)
    #
    # @classmethod
    # def createIndex(cls):
    #     # ===============
    #     # 인덱스 생성
    #     # ===============
    #     cls.es.indices.create(
    #         index = "today19020301",
    #         body = {
    #             "settings": {
    #               "number_of_shards": 5
    #             },
    #             "mappings": {
    #                 "today":{
    #                     "properties": {
    #                         "cont":    {"type": "text"},
    #                         "mnagnnm": {"type": "text"},
    #                         "post":    {"type": "text"},
    #                         "rgdt":    {"type": "text"},
    #                         "rgter":   {"type": "text"},
    #                         "tel":     {"type": "text"},
    #                         "title":   {"type": "text"}
    #                     }
    #                 }
    #             }
    #         }
    #     )





# ElaAPI.allIndex()
# ElaAPI.srvHealthCheck()
# ElaAPI.createIndex()
# ElaAPI.dataInsert()
ElaAPI.searchAll()
# ElaAPI.searchFilter()


#출처: https://sleep4725.tistory.com/entry/python-elasticsearch-조회삽입생성 [길]