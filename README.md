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

## 🛠️ Tech Stack
- **Database:** PostgreSQL (Star Schema)
- **ETL:** Python (Pandas, SQLAlchemy), Apache Airflow
- **BI:** Tableau Public
- **Orchestration:** Docker, GitHub Actions
- **Version Control:** Git/GitHub

## 📁 Project Structure
(Show the tree structure here)

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

