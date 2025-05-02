from pandas import DataFrame
from datetime import datetime
import warnings
import argparse
from jsonpath_ng import jsonpath, parse
from opensearchpy import OpenSearch
import pyarrow as pa
import pyarrow.parquet as pq
import re

parser = argparse.ArgumentParser()
parser.add_argument("--elasticsearchUrl","-e",help="OpenSearch URL",required=True)
parser.add_argument("--indexName","-i",help="Name of the OpenSearch index to extract",required=True)
parser.add_argument("--limit","-l",help="Limit number of rows (0 for all rows)",default=0,required=False)
parser.add_argument("--chunk",help="Chunk size",default=10000,required=False)

warnings.filterwarnings("ignore")

args = parser.parse_args()
def extractIndex(url,indexName,chunk_size,limit):
    es = OpenSearch(url)
    
    print("Search started", datetime.now())

    query = {
        "query": {
            "range": {
                "@timestamp": {
                    "gte": "2025-05-01T00:00:00.000",
                    "lt": "2025-05-02T00:00:00.000"
                }
            }
        }
    }
    res = es.search(index=indexName, scroll='10m', body=query, size=chunk_size)

    size = res["hits"]["total"]["value"]
    print(f"Got {size} hits")
    if limit > 0 :
        size = limit
    print(f"Getting {size} records")

    scroll_id = res['_scroll_id']
    print("Scroll id",scroll_id)
    print("Search finished",datetime.now())
    hits = res["hits"]["hits"]

    index_offset = 0
    while index_offset < size:
        print("Offset",index_offset)
        result = []
        for r in hits :
            index_offset += 1
            result.append(r["_source"])
            if index_offset >= size:
                print("Reached requested limit of", size)
                break

        prefix = re.sub(r"(?i)[^a-z0-9]", "", indexName)
        exportFileName = f"{prefix}.{index_offset}.parquet"
        print("Exporting to", exportFileName)
        df = DataFrame(result)
        table = pa.Table.from_pandas(df)
        pq.write_table(table, exportFileName)

        # fetch the next batch of results
        res = es.scroll(
            scroll_id=scroll_id,
            scroll='10m',  # time value for search
        )
        hits = res["hits"]["hits"]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    extractIndex(args.elasticsearchUrl,args.indexName,int(args.chunk),int(args.limit))
