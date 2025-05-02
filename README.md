# OpenSearch to parquet

OpenSearch to parquet is command line tool to offload OpenSearch index into a parquet file

These are some usage scenarios:

```
python main.py --elasticsearchUrl https://username:password@localhost:9200/  --indexName application_logs_idex
```

Also there are some extra parameters

````
--limit : if you want to limit number of exported documents , this parameter is generally used for testing purposes (default is unlimited)
````

```
--chunk : this parameter is used for adjusting scroll size for reading elasticsearch index (default is 1000)
```

# Dev container

Run all the python things in a container

```
./container.sh
python -m venv ./venv
source ./venv/bin/activate
pip install -r ./requirements.txt
```
