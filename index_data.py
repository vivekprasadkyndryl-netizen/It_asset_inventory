import csv
from elasticsearch import Elasticsearch, helpers

# Connect to Elasticsearch using API key
def get_client():
    return Elasticsearch(
        "https://my-elasticsearch-project-f6972f.es.us-central1.gcp.elastic.cloud:443",
        api_key="czg0bEtwb0JBczVkazk4SHpHa3k6anNaOS10aUhJUkttbFdxQ3JaVDBfQQ=="
    )

# Index name
INDEX_NAME = "it_asset_inventory"

# Load CSV and index data
def index_csv_to_elasticsearch(csv_file):
    es = get_client()
    
    # Create index if it doesn't exist
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME)

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        actions = [
            {
                "_index": INDEX_NAME,
                "_source": row
            }
            for row in reader
        ]
        helpers.bulk(es, actions)
        print(f"✅ Indexed {len(actions)} records into '{INDEX_NAME}'.")

if __name__ == "__main__":
    index_csv_to_elasticsearch("it_asset_inventory_cleaned.csv")
