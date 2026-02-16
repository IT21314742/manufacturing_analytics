# Manufacturing & Financial Data Analytics Hub

## 📊 Project Overview
end-to-end data pipeline platform that integrates manufacturing operational data with financial metrics. Built with Python, PostgreSQL, and Apache Airflow, it demonstrates modern data engineering practices including ETL orchestration, star schema warehousing, and business intelligence visualization.

The project showcases the complete data lifecycle from raw data ingestion through transformation to interactive dashboards—providing a scalable foundation for manufacturing performance analysis.

---

## 🎯 Project Goals

- Build a **production-ready ETL pipeline** for manufacturing data
- Implement a **star schema data warehouse** in PostgreSQL for analytical queries
- Demonstrate **workflow orchestration** with Apache Airflow
- Create **interactive BI dashboards** with Tableau Public
- Establish **CI/CD practices** using Docker and GitHub Actions
- Produce **actionable insights** combining manufacturing and financial metrics
---


## 🧠 How the Project Works

The system operates through three integrated layers:

### 1️⃣ Data Ingestion & Staging
Raw manufacturing data (production logs, machine sensors) and financial records are:
- Extracted from source files/APIs
- Validated for completeness and accuracy
- Staged in temporary tables for transformation


### 2️⃣ Transformation & Warehousing
The ETL process:
- Cleans and normalizes raw data
- Applies business logic and calculations
- Loads into a **star schema** with fact and dimension tables
- Maintains slowly changing dimensions for historical accuracy

### 3️⃣ Analytics & Visualization
The curated data enables:
- Production efficiency tracking (OEE, downtime analysis)
- Cost per unit calculations
- Revenue and profitability trends
- Interactive Tableau dashboards for decision support

---

## 🏗️ System Architecture Overview

At a high level, the system consists of:

- A **PostgreSQL database** with star schema design
- **Python ETL scripts** using Pandas and SQLAlchemy
- **Apache Airflow DAGs** for orchestration and scheduling
- **Tableau Public** for visualization and reporting
- **Docker containers** for consistent development/deployment
- **GitHub Actions** for automated testing and deployment


### Full System Architecture Diagram
![Architecture Diagram](docs/architecture.png)


## ⌛️ Runtime Sequence Explanation

The system follows this execution flow:

1. **Trigger** - Airflow DAG starts based on schedule or manual trigger
2. **Extract Phase** - Python scripts connect to data sources and pull raw data
3. **Staging** - Raw data is loaded into staging tables in PostgreSQL
4. **Transform Phase** - Data is cleaned, joined, and business logic is applied
5. **Load Phase** - Transformed data populates the star schema (fact/dimension tables)
6. **Validation** - Data quality checks ensure integrity and completeness
7. **Notification** - Success/failure alerts are logged and sent
8. **Visualization** - Tableau connects to the warehouse for dashboard updates

### Workflow States

The ETL pipeline transitions through these states:

- **🟡 Pending** - DAG initialized, waiting for execution
- **🔵 Running** - Tasks currently executing
- **🟢 Success** - All tasks completed successfully
- **🔴 Failed** - Error encountered, retry mechanism activated
- **🔄 Retrying** - Automatic retry of failed tasks
- **⏸️ Paused** - Manual pause of DAG execution

---

## 🛠️ Technology Stack

| Component          | Technology Choice                          |
|--------------------|---------------------------------------------|
| **Database**       | PostgreSQL 15+ (Star Schema Design)         |
| **ETL**            | Python 3.9+, Pandas, SQLAlchemy             |
| **Orchestration**  | Apache Airflow                              |
| **BI & Reporting** | Tableau Public                              |
| **Container**      | Docker, docker-compose                       |
| **CI/CD**          | GitHub Actions                              |
| **Version Control**| Git/GitHub                                  |
| **Monitoring**     | Airflow Logs, `etl_pipeline.log`              |

---


## 📁 Project Structure

```manufacturing_analytics/
│
├── 📂 src/ # Core ETL code
│ ├── 📂 extract/ # Data extraction modules
│ │ ├── extract_production.py
│ │ ├── extract_financial.py
│ │ └── extract_machine_data.py
│ │
│ ├── 📂 transform/ # Data transformation logic
│ │ ├── clean_data.py
│ │ ├── calculate_kpis.py
│ │ └── merge_datasets.py
│ │
│ └── 📂 load/ # Database loading scripts
│ ├── load_dimensions.py
│ └── load_facts.py
│
├── 📂 airflow/
│ └── 📂 dags/ # Airflow DAG definitions
│ ├── manufacturing_etl.py # Main ETL pipeline DAG
│ └── data_quality_dag.py # Data validation DAG
│
├── 📂 config/ # Configuration files
│ ├── database.ini # DB connection settings
│ └── logging.conf # Logging configuration
│
├── 📂 notebooks/ # Jupyter notebooks for exploration
│ └── exploratory_analysis.ipynb
│
├── 📂 docs/ # Documentation
│ └── data_dictionary.md # Schema documentation
│
├── 📂 tests/ # Unit and integration tests
│ ├── test_extract.py
│ ├── test_transform.py
│ └── test_load.py
│
├── 📂 .vscode/ # VS Code configuration
│ └── settings.json
│
├── 📄 PostgreSQL_Schema.sql # Complete database schema
├── 📄 DB_Manipulation_Queries.sql # Sample analytical queries
├── 📄 docker-compose.yml # Container orchestration
├── 📄 .env.example # Environment variables template
├── 📄 requirements.txt # Python dependencies
├── 📄 environment.yml # Conda environment
├── 📄 start_postgres.py # DB initialization helper
├── 📄 etl_pipeline.log # Pipeline execution logs
├── 📄 .gitattributes # Git attributes
├── 📄 .gitignore # Git ignore rules
└── 📄 README.md # You are here Mate!!
```

## 📦 Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 15+
- Docker (optional, for containerized setup)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/IT21314742/manufacturing_analytics.git
cd manufacturing_analytics
```

### Step 2: Set Up Python Environment
Using pip:
```
pip install -r requirements.txt
```

Using Conda:
```
conda env create -f environment.yml
conda activate manufacturing-analytics
```

### Step 3: Configure Database
1. Create a PostgreSQL database:
   ```
   CREATE DATABASE manufacturing_db;
   ```
## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 15+
- Git

### Installation
1. Clone repository:
```bash
git clone https://github.com/yourusername/manufacturing-analytics.git
cd manufacturing-analytics

