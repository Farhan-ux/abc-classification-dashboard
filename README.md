# ABC Classification Dashboard

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python&logoColor=white)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

An interactive Streamlit dashboard for visualizing and analyzing ABC inventory classifications. Upload your product data and instantly see category distributions, item breakdowns, and export filtered results.

## Features

- **File Upload Support** — CSV and Excel files with automatic column detection
- **Smart Column Mapping** — Auto-finds ASIN and Category columns even with non-standard names
- **Interactive Visualizations** — Donut charts, bar charts, and treemaps powered by Plotly
- **Category Filtering** — Filter by A (High Priority), B (Medium Priority), or C (Low Priority)
- **Full-text Search** — Search across ASINs in real time
- **Multi-format Export** — Download filtered data as CSV, Excel, or JSON
- **Sample Data Mode** — Demo mode with pre-generated sample data

## Installation

```bash
git clone https://github.com/Farhan-ux/abc-classification-dashboard.git
cd abc-classification-dashboard
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

1. Upload a CSV or Excel file containing ASIN and Category columns
2. Or check "Use Sample Data" for a quick demo
3. Explore the interactive charts and filtered table views
4. Export your filtered data in your preferred format

## Folder Structure

```
abc-classification-dashboard/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT License
└── README.md           # This file
```

## Requirements

- Python 3.8+
- Streamlit >= 1.28.0
- pandas >= 2.0.0
- plotly >= 5.15.0
- openpyxl >= 3.1.0

## File Format

Your upload file should contain:

| ASIN        | Category |
|-------------|----------|
| B01MSW8UNY  | A        |
| B01N4B2R3E  | B        |
| B09KCHC9TF  | C        |

The dashboard also recognizes variations like `Final_Category`, `Cat`, `Class` for the category column.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Author

**Farhan** — [GitHub](https://github.com/Farhan-ux)
