<div align="center">

# 🔄 Automated Cloud ETL Pipeline
### Python · GitHub Actions · Azure Data Lake Storage

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Azure](https://img.shields.io/badge/Azure_ADLS_Gen2-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

*Automatically extracts data from a public API, transforms it into clean tabular format, and loads it into Azure Data Lake — fully orchestrated via GitHub Actions CI/CD.*

</div>

---

## 📐 Architecture

<img width="1536" height="1024" alt="etl-pipeline architecture" src="https://github.com/user-attachments/assets/1ad923f2-7c58-4c91-888f-778a127aa8e6" />

---

## 📖 Overview

This project implements a beginner-friendly, cloud-native ETL pipeline that runs entirely in the cloud with zero manual intervention. On every push to `main` (or on a scheduled cron), GitHub Actions spins up a runner that:

1. **Extracts** raw JSON records from a public REST API
2. **Transforms** them into a clean, schema-validated Pandas DataFrame
3. **Loads** the result as a timestamped CSV into Azure Data Lake Storage Gen2

All credentials are managed via GitHub Secrets — nothing sensitive ever touches source control.

---

## ✨ Key Features

| Feature | Detail |
|---|---|
| 🤖 Automated Execution | Schedule or push-triggered via GitHub Actions |
| ☁️ Scalable Cloud Storage | Azure ADLS Gen2 with hierarchical namespace |
| 🔁 CI/CD Pipeline | Full test → build → deploy workflow |
| 🕐 Timestamped Ingestion | Each run produces a uniquely named output file |
| 🧩 Modular Codebase | Separate extract / transform / load modules |
| 🔐 Secure Secrets | Credentials stored as encrypted GitHub Secrets |
| 🧪 Unit Tested | Pytest suite validates transformation logic |
| 📋 Centralized Logging | Execution tracking across every pipeline stage |

---

## 🏗️ Project Structure

```text
etl-pipeline-project/
│
├── extractors/
│   └── api_extractor.py        # Fetches raw JSON from public API
│
├── transformers/
│   └── cleaner.py              # Cleans, renames, and enriches data
│
├── loaders/
│   └── adls_loader.py          # Uploads CSV to Azure ADLS Gen2
│
├── utils/
│   └── logger.py               # Centralized logging configuration
│
├── tests/
│   └── test_cleaner.py         # Pytest unit tests for transformations
│
├── .github/
│   └── workflows/
│       └── pipeline.yml        # GitHub Actions CI/CD workflow
│
├── .env                        # Local environment variables (not committed)
├── .gitignore
├── requirements.txt
├── main.py                     # Pipeline entry point
└── README.md
```

---

## 🔄 ETL Workflow

### 1. Extract — Fetch from API

Pulls raw JSON records from the public REST endpoint:

```
GET https://jsonplaceholder.typicode.com/posts
```

Returns a list of JSON objects that are passed directly to the transform stage.

---

### 2. Transform — Clean & Enrich

Applies the following transformations using Pandas:

- Column renaming to match the target schema
- Removal of null or invalid records
- Addition of derived fields (e.g. `title_word_count`)
- Schema standardisation and type casting

---

### 3. Load — Upload to Azure ADLS Gen2

The cleaned DataFrame is serialised to CSV and uploaded to the following ADLS path:

```
raw/
└── output/
    └── data_20260520T142000Z.csv   ← timestamped per run
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Data Processing | Pandas |
| HTTP Client | Requests |
| Cloud Storage | Azure Data Lake Storage Gen2 |
| CI/CD | GitHub Actions |
| Testing | Pytest |
| Secrets | GitHub Encrypted Secrets |
| Version Control | Git + GitHub |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- An Azure Storage Account with ADLS Gen2 enabled
- A GitHub repository with Actions enabled

---

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd etl-pipeline-project
```

### 2. Create a Virtual Environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account
AZURE_STORAGE_ACCOUNT_KEY=your_storage_key
ADLS_FILESYSTEM_NAME=raw
ADLS_OUTPUT_FOLDER=output
```

> ⚠️ **Never commit `.env` to source control.** It is listed in `.gitignore`.

---

## ▶️ Running Locally

```bash
python main.py
```

### Run Unit Tests

```bash
pytest tests/ -v
```

---

## 🔐 GitHub Secrets Configuration

Navigate to **Repository → Settings → Secrets and variables → Actions** and add:

| Secret Name | Description |
|---|---|
| `AZURE_STORAGE_ACCOUNT_NAME` | Azure Storage Account name |
| `AZURE_STORAGE_ACCOUNT_KEY` | Azure Storage Account access key |
| `ADLS_FILESYSTEM_NAME` | ADLS container (filesystem) name |
| `ADLS_OUTPUT_FOLDER` | Output folder path inside the container |

---

## 🤖 GitHub Actions Workflow

The pipeline runs automatically on every push to `main` or via manual dispatch.

```yaml
name: ETL Pipeline Deployment

on:
  push:
    branches:
      - main
  schedule:
    - cron: '0 6 * * *'   # Daily at 06:00 UTC
  workflow_dispatch:

jobs:
  run-etl-pipeline:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Run Unit Tests
        run: pytest tests/ -v

      - name: Run ETL Pipeline
        env:
          AZURE_STORAGE_ACCOUNT_NAME: ${{ secrets.AZURE_STORAGE_ACCOUNT_NAME }}
          AZURE_STORAGE_ACCOUNT_KEY: ${{ secrets.AZURE_STORAGE_ACCOUNT_KEY }}
          ADLS_FILESYSTEM_NAME: ${{ secrets.ADLS_FILESYSTEM_NAME }}
          ADLS_OUTPUT_FOLDER: ${{ secrets.ADLS_OUTPUT_FOLDER }}
        run: python main.py
```

**Workflow steps at a glance:**

```
Schedule / Push Trigger
        ↓
  Checkout Code
        ↓
   Setup Python
        ↓
Install Dependencies
        ↓
   Run Tests  ✅
        ↓
Run ETL Pipeline
        ↓
 Upload to ADLS ☁️
```

---

## 📋 Logging

Centralised logging is configured in `utils/logger.py` and covers every pipeline stage:

```
[INFO]  Pipeline started
[INFO]  Extracting data from API → https://jsonplaceholder.typicode.com/posts
[INFO]  100 records extracted successfully
[INFO]  Transforming and cleaning records...
[INFO]  Uploading to Azure ADLS Gen2: raw/output/data_20260520T142000Z.csv
[INFO]  Pipeline completed successfully ✅
```

Logs are also visible in the GitHub Actions run console for remote monitoring.

---

## 📄 Output

Each pipeline run generates a uniquely timestamped CSV:

```
data_20260520T142000Z.csv
```

**Output schema:**

| Column | Description |
|---|---|
| `id` | Record identifier |
| `user_id` | Source user identifier |
| `title` | Post title |
| `body` | Post body text |
| `title_word_count` | Derived — number of words in title |

---

## 🔮 Future Improvements

- [ ] Apache Airflow orchestration for complex DAGs
- [ ] Docker containerisation for portable execution
- [ ] PostgreSQL sink in addition to ADLS
- [ ] Parquet output format for columnar storage efficiency
- [ ] Medallion architecture (Bronze → Silver → Gold layers)
- [ ] Apache Kafka for real-time streaming ingestion
- [ ] Apache Spark for large-scale data processing
- [ ] Great Expectations for automated data quality validation

---

## 🧠 Skills Demonstrated

`ETL Pipelines` · `Cloud Storage Integration` · `CI/CD Automation` · `GitHub Actions` · `Python Scripting` · `Data Transformation` · `Unit Testing` · `Secrets Management` · `Azure Cloud Services` · `Logging & Observability`

---

## 👤 Author

