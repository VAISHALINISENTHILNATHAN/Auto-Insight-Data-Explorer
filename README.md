# Auto Insight Data Explorer

Auto Insight Data Explorer is a desktop application for **interactive data exploration**. Load CSV files and instantly get automated **EDA**, **insights**, **anomaly detection**, and **visualizations** through a clean, modern UI built with **KivyMD**.

---

## Features

- **CSV Import:** Load any CSV file using a user-friendly file dialog.  
- **Automated EDA:** Summarizes dataset with rows, columns, numeric/categorical columns, and basic statistics for each numeric column.  
- **Insights Generation:** Automatically highlights key patterns and observations in your data.  
- **Anomaly Detection:** Detects unusual or outlier rows with scores.  
- **Interactive Visualization:** Choose from Histograms, Line Plots, and Box Plots for all numeric columns.  
- **Modern UI:** Colorful, responsive, and easy-to-navigate screens built with KivyMD.  

---


## Installation

1. Clone this repository:

```bash
git clone /Auto-Insight-Data-Explorer.git
cd Auto-Insight-Data-Explorer

Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Install dependencies:
pip install -r requirements.txt
Dependencies may include: kivy, kivymd, matplotlib, pandas, numpy.

Run the app:
python main.py

Usage
Launch the app.

Click Load CSV or choose a file from the dialog.

Explore EDA, Insights, and Anomalies screens.

Go to Visualization to view Histograms, Line Plots, and Box Plots of numeric columns.

Project Structure
Auto-Insight-Data-Explorer/
├── core/
│   ├── loader.py
│   ├── config.py
│   ├── eda.py
│   ├── insights.py
│   └── anomalies.py
├── data/
│   └── sample.csv
├── main.py
├── requirements.txt
└── README.md
core/: Backend modules for loading data, EDA, insights, and anomaly detection.

data/: Sample CSV for testing.

main.py: Entry point of the application.

Contributing!!!
Contributions are welcome! Please open an issue or submit a pull request for:
Bug fixes
UI enhancements
New visualization types
Additional insight/anomaly methods
