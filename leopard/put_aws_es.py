#coding:utf-8
from elasticsearch import Elasticsearch,RequestsHttpConnection
from datetime import datetime

message = '2018-01-21 13:02:58 UTC:115.193.185.169(56040):root@web:[27117]:LOG:'\
        'duration: 18010.405 ms  statement: select R.group_id, product_id, R.count'
#message = '2018-01-21 13:02:58 UTC:115.193.185.169(56040):root@web:[27117]:LOG:'

end='search-log-ef44m247pre7wt32cdgfoejegq.us-west-2.es.amazonaws.com'
index_name = 'logstash-pg-slowlog-{0}'.format(datetime.now().strftime('%Y-%m-%d'))

def connectES(esEndPoint):
    try:
        esclient = Elasticsearch(
            hosts=[{'host':esEndPoint, 'port':443}],
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
            )
        print('ok')
        return esclient
    except Exception as e:
        print('Unable to connect to{0}'.format(esEndPoint))
        print(e)
        exit(3)
#connectES(end)

    indexDoc = {
                "dataRecord" : {
                    "properties" : {
                        "timestamp": {
                           "type" : "date"
                           #"format" : "dateOptionalTime"
                                   },
                        "message" : {
                            "type" :  "string",
                               }
                          }
                   }
                 }

def createIndex():
    esClient = connectES(end)
    index_name = 'logstash-pg-slowlog-{0}'.format(datetime.now().strftime('%Y-%m-%d'))
    #print index_name 
    res = esClient.indices.exists(index_name)
    if not res:
        try:
            esClient.indices.create(
                index = index_name,
                body = indexDoc
                     )
            print("create ok")
        except Exception as e:
            print("Unable to Create Index:e".format(e))
            exit(1)
    else:    
        print("Index already Exists!")
#createIndex()

def put_indexer():
    body = {
        'message':message,
        #'@timestamp':datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')
        'timestamp':datetime.now().isoformat()
         }
    EsClient = connectES(end)
    try:
        EsClient.index(
            index = index_name,
            doc_type = 'pg-slowlog',
            body = body
        )
        print('put indexe successd')
    except Exception as e:
        print("put indexer failed:{0}".format(e))
put_indexer()

'''
def run():
    createIndex()
    put_indexer()

run()
'''
