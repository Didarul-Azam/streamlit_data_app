# OHLCV Data Viewer - Streamlit App

A simple and interactive Streamlit application for viewing and analyzing OHLCV (Open, High, Low, Close, Volume) data from CSV files.

## Features

- 📊 **Data Upload**: Upload your own CSV files or use sample data
- 📋 **Interactive Table**: View data in a sortable, filterable table
- 📈 **Candlestick Charts**: Visualize price movements with candlestick charts
- 📊 **Volume Analysis**: View trading volume alongside price data
- 🔍 **Data Filtering**: Filter by symbol and date range
- 📥 **Data Export**: Download filtered data as CSV
- 📊 **Summary Statistics**: Get statistical overview of your data

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

3. **Upload your CSV file** or use the sample data provided

## CSV Format

Your CSV file should have the following columns:
- `Date`: Date in YYYY-MM-DD format
- `Symbol`: Stock/asset symbol (e.g., AAPL, MSFT)
- `Open`: Opening price
- `High`: Highest price of the day
- `Low`: Lowest price of the day
- `Close`: Closing price
- `Volume`: Trading volume

Example:
```csv
Date,Symbol,Open,High,Low,Close,Volume
2024-01-01,AAPL,150.25,152.80,149.90,151.75,45000000
2024-01-02,AAPL,151.80,153.20,150.50,152.30,42000000
```

## Sample Data

The app includes sample OHLCV data for AAPL and MSFT stocks from January 2024. You can use this to test the app before uploading your own data.

## Features Explained

### Data Overview
- **Total Records**: Number of data points
- **Unique Symbols**: Number of different stocks/assets
- **Date Range**: Time period covered by the data
- **Total Volume**: Sum of all trading volumes

### Data Filtering
- **Symbol Selection**: Choose which stocks to display
- **Date Range**: Select specific time periods to analyze

### Charts
- **Candlestick Chart**: Shows price movements with green (up) and red (down) candles
- **Volume Chart**: Displays trading volume as bars

### Summary Statistics
Provides statistical analysis including:
- Mean, standard deviation, minimum, and maximum for price data
- Sum, mean, and standard deviation for volume data

## Requirements

- Python 3.7+
- Streamlit 1.28.1
- Pandas 2.1.3
- Plotly 5.17.0

## Troubleshooting

- **File upload issues**: Ensure your CSV has the correct column names and format
- **Chart not displaying**: Make sure you've selected at least one symbol and valid date range
- **Performance issues**: For large datasets, consider filtering by date range to improve performance

## Customization

You can modify the app by:
- Adding more chart types (line charts, moving averages)
- Including technical indicators
- Adding more filtering options
- Customizing the UI theme

## License

This is a demo application for educational purposes. 