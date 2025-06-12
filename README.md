# 🛠️ Silo: Retail Data ETL Pipeline
A complete end-to-end ETL (Extract, Transform, Load) pipeline built to simulate a real-world retail analytics system. This project demonstrates key data engineering and BI skills using Python, Pandas, and Tableau.

This project is ideal for showcasing data pipeline design, API integration, and dashboarding skills in a clean, modular structure.

 ## 🗂️ Project Directory Structure 
 ``` ├── data/ │ ├── raw/ │ ├── processed/ │ └── final/ ├── etl/ │ ├── extract.py │ ├── transform.py │ └── load.py ├── dashboards/ │ └── retail_dashboard.pbix ├── .env ├── .gitignore ├── requirements.txt └── README.md ``` 

## ⚙️ Setup & Installation
### Clone the repository:
`git clone https://github.com/your-username/project-silo.git`
`cd project-silo`
### Install dependencies:
`pip install -r requirements.txt`

### Run ETL scripts:

`python etl/extract.py`
`python etl/transform.py`
`python etl/load.py`

## 💡 Key Features
🛠️ Modular Python ETL scripts

🌐 API extraction using requests

🧼 Pandas-based transformation logic

📤 XLSX export for dashboard tools

📊 Tableau dashboard for business insights

🔒 Secure handling of API keys with dotenv
