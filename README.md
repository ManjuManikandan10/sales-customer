# Sales Performance Dashboard (Python)

An interactive, professional sales dashboard built with Python (Streamlit and Plotly) for analyzing business performance across regions, categories, and timeframes.

[![Dashboard Preview](screenshots/dashboard_output.png)](http://localhost:8501)

## Features
- **Dynamic KPIs**: Instant view of Total Sales, Profit, Orders, and Marigin.
- **Regional Analysis**: Breakdown of sales performance by geographic region.
- **Category Insights**: Visualize which product categories drive the most revenue.
- **Trend Tracking**: Analyze monthly sales growth with interactive line charts.
- **Top Performers**: Identify the top 10 products contributing to profit.
- **Interactive Filters**: Refine view by Date range, Region, and Category.
- **Data Inspection**: View and sort the underlying transactional data.

## Project Structure
```text
Sales_Dashboard_Project/
├── app.py                  # Main Streamlit application
├── requirements.txt         # Python dependencies
├── data/
│   └── sales_data.csv      # Cleaned dataset
├── scripts/
│   └── data_manager.py     # Data generation & cleaning logic
└── screenshots/            # Dashboard mockups/images
```

## Setup & Running
1. **Clone the project** or copy the files.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Generate Data**:
   ```bash
   python scripts/data_manager.py
   ```
4. **Run Dashboard**:
   ```bash
   python -m streamlit run app.py
   ```

## Technologies Used
- **Streamlit**: For the interactive web interface.
- **Pandas**: For data manipulation and cleaning.
- **Plotly**: For high-quality, interactive visualizations.
