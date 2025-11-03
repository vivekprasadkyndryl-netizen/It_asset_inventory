from elasticsearch import Elasticsearch

# Connect to Elasticsearch
def get_client():
    return Elasticsearch(
        "https://my-elasticsearch-project-f6972f.es.us-central1.gcp.elastic.cloud:443",
        api_key="czg0bEtwb0JBczVkazk4SHpHa3k6anNaOS10aUhJUkttbFdxQ3JaVDBfQQ=="
    )

# Index names
SOURCE_INDEX = "it_asset_inventory"
TARGET_INDEX = "it_asset_inventory_enriched"

def reindex_data(es):
    # Reindex from source to target
    es.reindex(
        body={
            "source": {"index": SOURCE_INDEX},
            "dest": {"index": TARGET_INDEX}
        },
        wait_for_completion=True
    )
    print(f"✅ Reindexed data from '{SOURCE_INDEX}' to '{TARGET_INDEX}'.")

def enrich_data(es):
    # Add risk_level and system_age fields
    script = {
        "source": """
            if (ctx._source.containsKey('operating_system_lifecycle_status')) {
                def status = ctx._source.operating_system_lifecycle_status.toLowerCase();
                ctx._source.risk_level = (status == 'eol' || status == 'eos') ? 'High' : 'Low';
            } else {
                ctx._source.risk_level = 'Low';
            }

            if (ctx._source.containsKey('operating_system_installation_date')) {
                def installDate = LocalDate.parse(ctx._source.operating_system_installation_date);
                def now = LocalDate.now();
                ctx._source.system_age = ChronoUnit.YEARS.between(installDate, now);
            }
        """,
        "lang": "painless"
    }

    es.update_by_query(
        index=TARGET_INDEX,
        body={"script": script, "query": {"match_all": {}}},
        wait_for_completion=True
    )
    print("✅ Enriched records with 'risk_level' and 'system_age'.")

def delete_invalid_records(es):
    # Delete records with missing hostname or unknown provider
    query = {
        "bool": {
            "should": [
                {"bool": {"must_not": {"exists": {"field": "hostname"}}}},
                {"match": {"provider": "Unknown"}}
            ]
        }
    }

    es.delete_by_query(
        index=TARGET_INDEX,
        body={"query": query},
        wait_for_completion=True
    )
    print("✅ Deleted records with missing hostnames or unknown providers.")

if __name__ == "__main__":
    es = get_client()
    reindex_data(es)
    enrich_data(es)
    delete_invalid_records(es)
