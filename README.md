# 🛠️ Silo: Retail Data ETL & Analytics Pipeline

Silo is a simple yet powerful end-to-end ETL pipeline project designed to simulate a real-world retail data analytics workflow. It showcases how to collect data from APIs, clean and transform it using Python, and build interactive dashboards in Power BI.

Whether you're practicing for a data engineering role or showcasing your BI skills — this project is for you.

---

## 📦 What’s Included

- ✅ API data extraction (Mockaroo & Fake Store API)
- 🔧 Data transformation & cleaning with pandas
- 💾 Modular ETL scripts (extract, transform, load)
- 📊 Business dashboard in Power BI
- 🧪 Clean project structure & version control setup

---

## 📁 Project Structure

```
project-silo/
├── data/
│   ├── raw/            # Unprocessed API data
│   ├── processed/      # Cleaned, structured data
│   └── final/          # Data ready for BI tools
├── etl/
│   ├── extract.py      # Pulls data from APIs
│   ├── transform.py    # Cleans & enriches the data
│   └── load.py         # Saves final dataset for visualization
├── dashboards/
│   └── retail_orders_report.pbix  # Power BI dashboard file
├── .env                # API keys and environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Use

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/silo.git
cd silo
```

### 2. Run the ETL Pipeline
```bash
python etl/extract.py
python etl/transform.py
python etl/load.py
```

---

🧠 Build. Clean. Visualize. Repeat.

