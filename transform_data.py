# from elasticsearch import Elasticsearch
# import time

# # Connect to Elasticsearch
# def get_client():
#     return Elasticsearch(
#         "https://my-elasticsearch-project-f6972f.es.us-central1.gcp.elastic.cloud:443",
#         api_key="czg0bEtwb0JBczVkazk4SHpHa3k6anNaOS10aUhJUkttbFdxQ3JaVDBfQQ=="
#     )

# # Index names
# SOURCE_INDEX = "it_asset_inventory"
# TARGET_INDEX = "it_asset_inventory_enriched"

# # Define mappings
# mappings = {
#     "mappings": {
#         "properties": {
#             "hostname": {"type": "keyword"},
#             "country": {"type": "keyword"},
#             "operating_system_name": {"type": "keyword"},
#             "operating_system_provider": {"type": "keyword"},
#             "operating_system_installation_date": {"type": "date"},
#             "operating_system_lifecycle_status": {"type": "keyword"},
#             "os_is_virtual": {"type": "boolean"},
#             "is_internet_facing": {"type": "boolean"},
#             "image_purpose": {"type": "keyword"},
#             "os_system_id": {"type": "keyword"},
#             "performance_score": {"type": "float"},
#             "risk_level": {"type": "keyword"},
#             "system_age": {"type": "float"},
#         }
#     }
# }

# def create_or_reset_index(es):
#     if es.indices.exists(index=TARGET_INDEX):
#         es.indices.delete(index=TARGET_INDEX)
#         print(f"Deleted existing index '{TARGET_INDEX}'.")

#     es.indices.create(index=TARGET_INDEX, body=mappings)
#     print(f"Created index '{TARGET_INDEX}' with mappings.")

# def reindex_data(es):
#     es.reindex(
#         body={
#             "source": {"index": SOURCE_INDEX},
#             "dest": {"index": TARGET_INDEX},
#             "script": {
#                 "lang": "painless",
#                 "source": """
#                     if (ctx._source.containsKey('os_is_virtual')) {
#                         def val = ctx._source.os_is_virtual.toString().toLowerCase();
#                         ctx._source.os_is_virtual = (val == 'true');
#                     }
#                     if (ctx._source.containsKey('is_internet_facing')) {
#                         def val = ctx._source.is_internet_facing.toString().toLowerCase();
#                         ctx._source.is_internet_facing = (val == 'true');
#                     }
#                 """
#             }
#         },
#         wait_for_completion=True,
#         refresh=True
#     )
#     print(f"Reindexed data from '{SOURCE_INDEX}' to '{TARGET_INDEX}' with boolean normalization.")

# def delete_invalid_records(es):
#     query = {
#         "query": {
#             "bool": {
#                 "should": [
#                     {"bool": {"must_not": {"exists": {"field": "hostname"}}}},
#                     {"match": {"operating_system_provider": "Unknown"}},
#                     {"match": {"hostname": "Unknown"}}
#                 ]
#             }
#         }
#     }

#     es.delete_by_query(
#         index=TARGET_INDEX,
#         body=query,
#         wait_for_completion=True,
#         refresh=True
#     )
#     print("Deleted records with missing or unknown fields.")

# def enrich_data(es):
#     script = {
#         "script": {
#             "params": {"now": int(time.time())},
#             "source": """
#                 if (ctx._source.operating_system_lifecycle_status == 'EOL' || 
#                     ctx._source.operating_system_lifecycle_status == 'EOS') {
#                     ctx._source.risk_level = 'High';
#                 } else {
#                     ctx._source.risk_level = 'Low';
#                 }

#                 def installDate = Instant.parse(ctx._source.operating_system_installation_date + "T00:00:00Z");
#                 def nowInstant = Instant.ofEpochSecond(params.now);
#                 long daysBetween = ChronoUnit.DAYS.between(installDate, nowInstant);
#                 ctx._source.system_age = daysBetween / 365.0;
#             """
#         }
#     }

#     es.update_by_query(
#         index=TARGET_INDEX,
#         body=script,
#         wait_for_completion=True,
#         refresh=True
#     )
#     print("Enriched records with 'risk_level' and 'system_age'.")

# if __name__ == "__main__":
#     es = get_client()
#     create_or_reset_index(es)
#     reindex_data(es)
#     delete_invalid_records(es)
#     enrich_data(es)
#     print(" Reindexing and enrichment complete.")


from elasticsearch import Elasticsearch
import time

# Connect to Elasticsearch
def get_client():
    return Elasticsearch(
        "https://my-elasticsearch-project-f6972f.es.us-central1.gcp.elastic.cloud:443",
        api_key="czg0bEtwb0JBczVkazk4SHpHa3k6anNaOS10aUhJUkttbFdxQ3JaVDBfQQ=="
    )

# Index names
SOURCE_INDEX = "it_asset_inventory"
TARGET_INDEX = "it_asset_inventory_enriched"

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
            "performance_score": {"type": "float"},
            "risk_level": {"type": "keyword"},
            "system_age": {"type": "float"}
        }
    }
}

def create_or_reset_index(es):
    if es.indices.exists(index=TARGET_INDEX):
        es.indices.delete(index=TARGET_INDEX)
        print(f"Deleted existing index '{TARGET_INDEX}'.")

    es.indices.create(index=TARGET_INDEX, body=mappings)
    print(f"Created index '{TARGET_INDEX}' with mappings.")

def reindex_data(es):
    es.reindex(
        body={
            "source": {"index": SOURCE_INDEX},
            "dest": {"index": TARGET_INDEX},
            "script": {
                "lang": "painless",
                "source": """
                    if (ctx._source.containsKey('os_is_virtual')) {
                        def val = ctx._source.os_is_virtual.toString().toLowerCase();
                        ctx._source.os_is_virtual = (val == 'true');
                    }
                    if (ctx._source.containsKey('is_internet_facing')) {
                        def val = ctx._source.is_internet_facing.toString().toLowerCase();
                        ctx._source.is_internet_facing = (val == 'true');
                    }
                """
            }
        },
        wait_for_completion=True,
        refresh=True
    )
    print(f"Reindexed data from '{SOURCE_INDEX}' to '{TARGET_INDEX}' with boolean normalization.")

def delete_invalid_records(es):
    query = {
        "query": {
            "bool": {
                "should": [
                    {"bool": {"must_not": {"exists": {"field": "hostname"}}}},
                    {"match": {"operating_system_provider": "Unknown"}},
                    {"match": {"hostname": "Unknown"}}
                ]
            }
        }
    }

    es.delete_by_query(
        index=TARGET_INDEX,
        body=query,
        wait_for_completion=True,
        refresh=True
    )
    print("Deleted records with missing or unknown fields.")

def enrich_data(es):
    script = {
        "script": {
            "params": {"now": int(time.time())},
            "source": """
                if (ctx._source.containsKey('operating_system_lifecycle_status')) {
                    def status = ctx._source.operating_system_lifecycle_status.toLowerCase();
                    ctx._source.risk_level = (status == 'eol' || status == 'eos') ? 'High' : 'Low';
                } else {
                    ctx._source.risk_level = 'Low';
                }

                if (ctx._source.containsKey('operating_system_installation_date')) {
                    def installDate = Instant.parse(ctx._source.operating_system_installation_date + "T00:00:00Z");
                    def nowInstant = Instant.ofEpochSecond(params.now);
                    long daysBetween = ChronoUnit.DAYS.between(installDate, nowInstant);
                    ctx._source.system_age = daysBetween / 365.0;
                }
            """
        }
    }

    es.update_by_query(
        index=TARGET_INDEX,
        body=script,
        wait_for_completion=True,
        refresh=True
    )
    print("Enriched records with 'risk_level' and 'system_age'.")

if __name__ == "__main__":
    es = get_client()
    create_or_reset_index(es)
    reindex_data(es)
    delete_invalid_records(es)
    enrich_data(es)
    print("Reindexing and enrichment complete.")