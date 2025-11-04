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

# Define mappings
mappings = {
    "mappings": {
        "properties": {
            "hostname": {"type": "keyword"},
            "country": {"type": "keyword"},
            "operating_system_name": {"type": "keyword"},
            "operating_system_provider": {"type": "keyword"},
            "operating_system_installation_date": {"type": "date"},
            "operating_system_lifecycle_status": {"type": "keyword"},
            "os_is_virtual": {"type": "boolean"},
            "is_internet_facing": {"type": "boolean"},
            "image_purpose": {"type": "keyword"},
            "os_system_id": {"type": "keyword"},
            "performance_score": {"type": "float"}
        }
    }
}

# Load CSV and index data
def index_csv_to_elasticsearch(csv_file):
    es = get_client()

    # Delete index if it exists
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        print(f"Deleted existing index '{INDEX_NAME}'.")

    # Create index with mappings
    es.indices.create(index=INDEX_NAME, body=mappings)
    print(f"Created index '{INDEX_NAME}' with mappings.")

    # Read and normalize CSV data
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        actions = []

        for row in reader:
            # Normalize boolean fields
            row["os_is_virtual"] = row["os_is_virtual"].strip().lower() == "true"
            row["is_internet_facing"] = row["is_internet_facing"].strip().lower() == "true"

            # Convert performance_score to float if present
            if "performance_score" in row and row["performance_score"]:
                try:
                    row["performance_score"] = float(row["performance_score"])
                except ValueError:
                    row["performance_score"] = None

            actions.append({
                "_index": INDEX_NAME,
                "_source": row
            })

        helpers.bulk(es, actions)
        print(f"Indexed {len(actions)} records into '{INDEX_NAME}'.")

if __name__ == "__main__":
    index_csv_to_elasticsearch("it_asset_inventory_cleaned-2.csv")