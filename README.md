# 🛠️ Silo: Retail Data ETL Pipeline
A complete end-to-end ETL (Extract, Transform, Load) pipeline built to simulate a real-world retail analytics system. This project demonstrates key data engineering and BI skills using Python, Pandas, and Tableau.

This project is ideal for showcasing data pipeline design, API integration, and dashboarding skills in a clean, modular structure.

## 🗂️ Directory Structure
graphql
Copy
Edit
project-silo/
├── data/
│   ├── raw/               # Raw JSON data from Mockaroo
│   ├── processed/         # Cleaned intermediate JSON
│   └── final/             # Final XLSX file for Tableau
├── etl/
│   ├── extract.py         # Script to extract API data
│   ├── transform.py       # Script to clean and transform data
│   └── load.py            # Script to export final dataset
├── dashboards/
│   └── retail_dashboard.twb  # Tableau workbook file
├── .env                   # API keys (excluded via .gitignore)
├── .gitignore
├── requirements.txt       # Python dependencies
└── README.md   


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
