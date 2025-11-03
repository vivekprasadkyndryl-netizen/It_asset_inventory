# IT Asset Inventory Management System

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.x-orange.svg)](https://www.elastic.co/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive data operations project for managing IT asset inventory using Python and Elasticsearch. This system provides automated data ingestion, transformation, enrichment, and analysis of IT infrastructure assets across multiple countries and environments.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Data Schema](#data-schema)
- [Elasticsearch Operations](#elasticsearch-operations)
- [Data Transformations](#data-transformations)
- [Querying and Analysis](#querying-and-analysis)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project implements a complete data pipeline for IT asset inventory management, featuring:

- **Data Ingestion**: Automated loading of CSV data into Elasticsearch
- **Data Transformation**: Enrichment with calculated fields like risk levels and system age
- **Data Quality**: Automated cleanup of invalid or incomplete records
- **Cloud Deployment**: Integration with Elasticsearch Cloud (GCP)
- **Real-time Analysis**: Query capabilities for asset monitoring and compliance

### Use Cases

- IT infrastructure monitoring and audit compliance
- Lifecycle management for operating systems
- Risk assessment based on EOL/EOS status
- Geographic distribution analysis of IT assets
- Performance tracking and optimization

## ✨ Features

### Core Capabilities

- ✅ **Bulk Data Indexing**: Efficiently load large CSV datasets into Elasticsearch
- ✅ **Data Enrichment**: Automatically calculate risk levels and system age
- ✅ **Data Quality Management**: Remove invalid records with missing critical fields
- ✅ **Reindexing Pipeline**: Seamless data migration between indices
- ✅ **Cloud Integration**: Production-ready deployment on Elasticsearch Cloud
- ✅ **Comprehensive Logging**: Track all operations with detailed status messages

### Data Transformations

- **Risk Level Assessment**: Automatic classification based on lifecycle status (EOL/EOS = High Risk)
- **System Age Calculation**: Years since OS installation
- **Data Validation**: Removal of records with unknown providers or missing hostnames
- **Field Standardization**: Consistent data types and formats

## 🏗️ Architecture

```
┌─────────────────┐
│   CSV Source    │
│  (Raw Data)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  index_data.py  │ ◄── Phase 1: Data Ingestion
│  (Data Loading) │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   Elasticsearch         │
│   it_asset_inventory    │ ◄── Source Index
└────────┬────────────────┘
         │
         ▼
┌─────────────────┐
│transform_data.py│ ◄── Phase 2: Data Transformation
│ (Enrichment)    │
└────────┬────────┘
         │
         ▼
┌──────────────────────────┐
│   Elasticsearch          │
│ it_asset_inventory_      │ ◄── Target Index (Enriched)
│   enriched               │
└──────────────────────────┘
```

## 🔧 Prerequisites

### Required Software

- **Python**: 3.7 or higher
- **Elasticsearch**: 8.x (Cloud or Self-hosted)
- **pip**: Python package manager

### Python Packages

```bash
elasticsearch>=8.0.0
```

### Elasticsearch Setup

You need access to an Elasticsearch cluster. Options:

1. **Elasticsearch Cloud** (Recommended for production)
   - Sign up at [elastic.co/cloud](https://cloud.elastic.co/)
   - Create a deployment
   - Generate API key

2. **Local Installation**
   - Download from [elastic.co/downloads](https://www.elastic.co/downloads/elasticsearch)
   - Run locally on `localhost:9200`

3. **Docker**
   ```bash
   docker run -d --name elasticsearch \
     -p 9200:9200 -p 9300:9300 \
     -e "discovery.type=single-node" \
     -e "xpack.security.enabled=false" \
     docker.elastic.co/elasticsearch/elasticsearch:8.11.0
   ```

## 📥 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/vivekprasadkyndryl-netizen/It_asset_inventory.git
cd It_asset_inventory
```

### 2. Install Dependencies

```bash
pip install elasticsearch
```

Or if you have a requirements file:

```bash
pip install -r requirements.txt
```

### 3. Configure Elasticsearch Connection

Update the connection details in both `index_data.py` and `transform_data.py`:

```python
def get_client():
    return Elasticsearch(
        "YOUR_ELASTICSEARCH_URL",
        api_key="YOUR_API_KEY"
    )
```

**For Local Elasticsearch:**
```python
def get_client():
    return Elasticsearch(["http://localhost:9200"])
```

## 📁 Project Structure

```
It_asset_inventory/
│
├── index_data.py                      # Phase 1: Data ingestion script
├── transform_data.py                  # Phase 2: Data transformation script
├── it_asset_inventory_cleaned.csv    # Source data (cleaned)
├── Report.pdf                         # Project documentation/report
├── README.md                          # This file
└── .git/                              # Git repository
```

### File Descriptions

| File | Purpose | Phase |
|------|---------|-------|
| `index_data.py` | Loads CSV data into Elasticsearch | Phase 1 - Ingestion |
| `transform_data.py` | Enriches and transforms indexed data | Phase 2 - Transformation |
| `it_asset_inventory_cleaned.csv` | Cleaned IT asset inventory data | Data Source |
| `Report.pdf` | Project report and analysis | Documentation |

## 🚀 Usage

### Phase 1: Data Indexing

Load the CSV data into Elasticsearch:

```bash
python index_data.py
```

**What it does:**
1. Connects to Elasticsearch using API key
2. Creates the `it_asset_inventory` index if it doesn't exist
3. Reads data from `it_asset_inventory_cleaned.csv`
4. Bulk indexes all records into Elasticsearch
5. Displays success message with record count

**Expected Output:**
```
✅ Indexed 329 records into 'it_asset_inventory'.
```

### Phase 2: Data Transformation

Transform and enrich the indexed data:

```bash
python transform_data.py
```

**What it does:**
1. **Reindex**: Copies data from `it_asset_inventory` to `it_asset_inventory_enriched`
2. **Enrich**: Adds calculated fields:
   - `risk_level`: "High" for EOL/EOS systems, "Low" otherwise
   - `system_age`: Years since OS installation
3. **Clean**: Removes records with missing hostnames or unknown providers

**Expected Output:**
```
✅ Reindexed data from 'it_asset_inventory' to 'it_asset_inventory_enriched'.
✅ Enriched records with 'risk_level' and 'system_age'.
✅ Deleted records with missing hostnames or unknown providers.
```

### Complete Pipeline

Run both phases in sequence:

```bash
python index_data.py
python transform_data.py
```

## 📊 Data Schema

### Source Data Fields (CSV)

| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `Hostname` | string | Server hostname | host-6930 |
| `Country` | string | Server location | USA, INDIA, UK |
| `Operating_system_name` | string | OS name | RHEL 8, Ubuntu 22.04 |
| `Operating_system_provider` | string | OS vendor | RedHat, Microsoft |
| `operating_system_installation_date` | date | Install date | 2016-02-10 |
| `operating_system_lifecycle_status` | string | Lifecycle status | Active, EOL, EOS, Planned |
| `os_is_virtual` | boolean | Virtual machine? | TRUE, FALSE |
| `is_internet_facing` | string | Internet access | Yes, No |
| `image_purpose` | string | Environment type | Production, Dev, Testing, DR |
| `os_system_id` | string | Unique system ID | SYS-30313 |
| `performance_score` | float | Performance metric | 55.48 |

### Enriched Fields (Added by transform_data.py)

| Field Name | Type | Description | Calculation |
|------------|------|-------------|-------------|
| `risk_level` | string | Security risk level | "High" if status is EOL/EOS, else "Low" |
| `system_age` | integer | Years since installation | Current year - Installation year |

## 🔍 Elasticsearch Operations

### Index Information

**Source Index:** `it_asset_inventory`
- Contains raw data loaded from CSV
- All original fields preserved
- Used as the source for transformations

**Target Index:** `it_asset_inventory_enriched`
- Contains transformed and enriched data
- Includes additional calculated fields
- Cleaned of invalid records
- Production-ready for analysis

### Checking Index Health

```bash
# Get index stats
curl -X GET "YOUR_ES_URL/it_asset_inventory/_stats?pretty"

# Count documents
curl -X GET "YOUR_ES_URL/it_asset_inventory/_count?pretty"

# View index mapping
curl -X GET "YOUR_ES_URL/it_asset_inventory/_mapping?pretty"
```

### Using Python Client

```python
from elasticsearch import Elasticsearch

es = Elasticsearch(
    "YOUR_ELASTICSEARCH_URL",
    api_key="YOUR_API_KEY"
)

# Check connection
print(es.ping())

# Get document count
count = es.count(index="it_asset_inventory")
print(f"Total documents: {count['count']}")

# Get sample document
result = es.search(index="it_asset_inventory", size=1)
print(result['hits']['hits'][0]['_source'])
```

## 🔄 Data Transformations

### 1. Risk Level Calculation

**Logic:**
```python
if operating_system_lifecycle_status in ['EOL', 'EOS']:
    risk_level = 'High'
else:
    risk_level = 'Low'
```

**Business Impact:**
- Identifies systems requiring immediate attention
- Enables prioritization of upgrade schedules
- Supports compliance reporting

### 2. System Age Calculation

**Logic:**
```python
system_age = current_year - installation_year
```

**Business Impact:**
- Tracks aging infrastructure
- Plans hardware refresh cycles
- Identifies outdated systems

### 3. Data Quality Cleanup

**Removed Records:**
- Missing hostname field
- Provider marked as "Unknown"

**Rationale:**
- Ensures data reliability
- Improves query performance
- Maintains data integrity

## 📈 Querying and Analysis

### Basic Queries

#### 1. Count All Assets
```python
es.count(index="it_asset_inventory_enriched")
```

#### 2. Get All High-Risk Systems
```python
es.search(
    index="it_asset_inventory_enriched",
    body={
        "query": {
            "term": {"risk_level": "High"}
        }
    }
)
```

#### 3. Find Systems by Country
```python
es.search(
    index="it_asset_inventory_enriched",
    body={
        "query": {
            "term": {"Country": "USA"}
        }
    }
)
```

#### 4. Get Systems Older Than 5 Years
```python
es.search(
    index="it_asset_inventory_enriched",
    body={
        "query": {
            "range": {
                "system_age": {"gte": 5}
            }
        }
    }
)
```

### Aggregation Queries

#### Assets by Country
```python
es.search(
    index="it_asset_inventory_enriched",
    body={
        "size": 0,
        "aggs": {
            "by_country": {
                "terms": {"field": "Country"}
            }
        }
    }
)
```

#### Risk Distribution
```python
es.search(
    index="it_asset_inventory_enriched",
    body={
        "size": 0,
        "aggs": {
            "risk_distribution": {
                "terms": {"field": "risk_level"}
            }
        }
    }
)
```

#### Average System Age by OS
```python
es.search(
    index="it_asset_inventory_enriched",
    body={
        "size": 0,
        "aggs": {
            "by_os": {
                "terms": {"field": "Operating_system_name"},
                "aggs": {
                    "avg_age": {
                        "avg": {"field": "system_age"}
                    }
                }
            }
        }
    }
)
```

### Sample cURL Commands

```bash
# Get high-risk systems
curl -X GET "YOUR_ES_URL/it_asset_inventory_enriched/_search?pretty" \
-H 'Content-Type: application/json' -d'
{
  "query": {
    "term": {"risk_level": "High"}
  }
}'

# Get systems by purpose
curl -X GET "YOUR_ES_URL/it_asset_inventory_enriched/_search?pretty" \
-H 'Content-Type: application/json' -d'
{
  "query": {
    "term": {"image_purpose": "Production"}
  }
}'

# Count EOL systems
curl -X GET "YOUR_ES_URL/it_asset_inventory_enriched/_count?pretty" \
-H 'Content-Type: application/json' -d'
{
  "query": {
    "term": {"operating_system_lifecycle_status": "EOL"}
  }
}'
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. Connection Error: "Connection refused"

**Problem:** Cannot connect to Elasticsearch

**Solutions:**
```bash
# Check if Elasticsearch is running
curl http://localhost:9200

# Verify the URL and port
# For cloud: Check your deployment URL in Elastic Cloud console
# For local: Ensure service is started
```

#### 2. Authentication Error: "401 Unauthorized"

**Problem:** Invalid API key or credentials

**Solutions:**
- Regenerate API key in Elasticsearch Cloud console
- Verify API key has proper permissions (read, write, manage)
- For local ES, check if security is enabled

#### 3. Index Already Exists Error

**Problem:** Trying to create an index that already exists

**Solutions:**
```python
# Delete existing index
es.indices.delete(index="it_asset_inventory", ignore=[404])

# Or use update logic
if es.indices.exists(index="it_asset_inventory"):
    es.indices.delete(index="it_asset_inventory")
es.indices.create(index="it_asset_inventory")
```

#### 4. CSV File Not Found

**Problem:** `FileNotFoundError` when running index_data.py

**Solutions:**
```bash
# Verify file exists
ls it_asset_inventory_cleaned.csv

# Check current directory
pwd

# Use absolute path in script
csv_file = "C:/full/path/to/it_asset_inventory_cleaned.csv"
```

#### 5. Import Error: "No module named 'elasticsearch'"

**Problem:** Elasticsearch Python client not installed

**Solutions:**
```bash
# Install the package
pip install elasticsearch

# Verify installation
pip show elasticsearch

# Upgrade if needed
pip install --upgrade elasticsearch
```

#### 6. Script Syntax Error

**Problem:** Painless script errors in transform_data.py

**Solutions:**
- Ensure Elasticsearch version is 8.x or higher
- Check field names match exactly (case-sensitive)
- Test script with smaller dataset first

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Best Practices

### 1. Security
- ✅ Never commit API keys to Git
- ✅ Use environment variables for credentials
- ✅ Implement role-based access control
- ✅ Enable SSL/TLS for connections

### 2. Performance
- ✅ Use bulk operations for large datasets
- ✅ Index with appropriate mappings
- ✅ Monitor index size and shard count
- ✅ Use filters before queries for better performance

### 3. Data Quality
- ✅ Validate data before indexing
- ✅ Handle missing values gracefully
- ✅ Document data transformations
- ✅ Maintain data lineage

### 4. Maintenance
- ✅ Regular index optimization
- ✅ Monitor cluster health
- ✅ Backup important indices
- ✅ Document API version dependencies

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Ideas

- Add data validation layer
- Implement automated testing
- Create visualization dashboards
- Add support for other data sources
- Enhance error handling
- Add CI/CD pipeline

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Vivek Kumar Prasad** - [vivekprasadkyndryl-netizen](https://github.com/vivekprasadkyndryl-netizen)

## 🙏 Acknowledgments

- Elasticsearch team for excellent documentation
- Python community for helpful libraries
- Kyndryl for project support and infrastructure

## 📞 Support

For questions, issues, or suggestions:

- **GitHub Issues**: [Create an issue](https://github.com/vivekprasadkyndryl-netizen/It_asset_inventory/issues)
- **Email**: Contact through GitHub profile
- **Documentation**: Refer to [Elasticsearch Documentation](https://www.elastic.co/guide/index.html)

## 📊 Project Status

- ✅ Phase 1: Data Ingestion - **Completed**
- ✅ Phase 2: Data Transformation - **Completed**
- 🔄 Phase 3: Visualization Dashboard - **Planned**
- 🔄 Phase 4: Automated Monitoring - **Planned**

## 🔗 Related Resources

- [Elasticsearch Python Client](https://elasticsearch-py.readthedocs.io/)
- [Elasticsearch Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)
- [Painless Scripting](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-painless.html)
- [Elastic Cloud](https://cloud.elastic.co/)

---

**Last Updated:** November 2025

**Version:** 1.0.0

**Status:** Active Development

Made with ❤️ for IT Infrastructure Management
