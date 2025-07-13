import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from datetime import timedelta
import time

# Set page config
st.set_page_config(
    page_title="OHLCV Data Viewer",
    page_icon="📈",
    layout="wide"
)

# --- Authentication Setup ---
CREDENTIALS_FILE = 'hashed_credentials.yml'
if not os.path.exists(CREDENTIALS_FILE):
    st.error(f"❌ Credentials file '{CREDENTIALS_FILE}' not found. Please generate it using 'generate_hashed_credentials.py'.")
    st.stop()
with open(CREDENTIALS_FILE, 'r') as file:
    config = yaml.safe_load(file)

# Use config loaded from file
if 'cookie' not in config:
    config['cookie'] = {
        'expiry_days': 0.208,  # 5 hours
        'key': 'some_signature_key',
        'name': 'auth_cookie'
    }

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    auto_hash=False
)

try:
    authenticator.login()
except Exception as e:
    st.error(e)
authentication_status = st.session_state.get('authentication_status')

# --- Idle Timeout ---
# Initialize last activity if not exists
if 'last_activity' not in st.session_state:
    st.session_state['last_activity'] = time.time()
# Reset last activity on any interaction
st.session_state['last_activity'] = time.time()

# Check idle timeout (10 minutes = 600 seconds)
if authentication_status:
    if time.time() - st.session_state['last_activity'] > 600:
        authenticator.logout()
        st.warning('Session timed out due to inactivity. Please log in again.')
        st.stop()

if authentication_status == False:
    st.error('Username/password is incorrect')
    st.stop()
if authentication_status == None:
    st.warning('Please enter your username and password')
    st.stop()

# --- Main App (only after login) ---
authenticator.logout('Logout')

# Title and description
st.title("📈 OHLCV Data Viewer")
st.markdown("A simple Streamlit app to view and analyze OHLCV (Open, High, Low, Close, Volume) data from CSV files.")

# File upload section
st.header("📁 Data Upload")
uploaded_file = st.file_uploader(
    "Choose a CSV file with OHLCV data",
    type=['csv'],
    help="Upload a CSV file with columns: Date, Symbol, Open, High, Low, Close, Volume"
)

# Default to sample data if no file uploaded
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        df = None
else:
    # Load sample data
    if os.path.exists('sample_ohlcv_data.csv'):
        df = pd.read_csv('sample_ohlcv_data.csv')
        st.info("📊 Using sample data. Upload your own CSV file to analyze your data.")
    else:
        st.error("❌ No sample data found. Please upload a CSV file.")
        df = None

if df is not None:
    # Data preprocessing
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(['Symbol', 'Date'])
    
    # Display basic info
    st.header("📊 Data Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Unique Symbols", df['Symbol'].nunique())
    with col3:
        st.metric("Date Range", f"{df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
    with col4:
        st.metric("Total Volume", f"{df['Volume'].sum():,.0f}")
    
    # Symbol filter
    st.header("🔍 Data Filtering")
    symbols = df['Symbol'].unique()
    selected_symbols = st.multiselect(
        "Select symbols to display:",
        symbols,
        default=symbols[:2] if len(symbols) >= 2 else symbols
    )
    
    # Date range filter
    date_range = st.date_input(
        "Select date range:",
        value=(df['Date'].min().date(), df['Date'].max().date()),
        min_value=df['Date'].min().date(),
        max_value=df['Date'].max().date()
    )
    
    # Filter data
    if selected_symbols and len(date_range) == 2:
        filtered_df = df[
            (df['Symbol'].isin(selected_symbols)) &
            (df['Date'].dt.date >= date_range[0]) &
            (df['Date'].dt.date <= date_range[1])
        ]
        
        if not filtered_df.empty:
            # Display data table
            st.header("📋 Data Table")
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Download button
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download filtered data as CSV",
                data=csv,
                file_name=f"ohlcv_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            # Charts section
            st.header("📈 Charts")
            
            # Price chart
            if len(selected_symbols) > 0:
                fig = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.03,
                    subplot_titles=('Price Chart', 'Volume Chart'),
                    row_width=[0.7, 0.3]
                )
                
                for symbol in selected_symbols:
                    symbol_data = filtered_df[filtered_df['Symbol'] == symbol]
                    
                    # Candlestick chart
                    fig.add_trace(
                        go.Candlestick(
                            x=symbol_data['Date'],
                            open=symbol_data['Open'],
                            high=symbol_data['High'],
                            low=symbol_data['Low'],
                            close=symbol_data['Close'],
                            name=symbol,
                            increasing_line_color='#00ff00',
                            decreasing_line_color='#ff0000'
                        ),
                        row=1, col=1
                    )
                    
                    # Volume bars
                    fig.add_trace(
                        go.Bar(
                            x=symbol_data['Date'],
                            y=symbol_data['Volume'],
                            name=f"{symbol} Volume",
                            opacity=0.7
                        ),
                        row=2, col=1
                    )
                
                fig.update_layout(
                    title=f"OHLCV Chart for {', '.join(selected_symbols)}",
                    xaxis_rangeslider_visible=False,
                    height=600
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Summary statistics
            st.header("📊 Summary Statistics")
            summary_stats = filtered_df.groupby('Symbol').agg({
                'Open': ['mean', 'std', 'min', 'max'],
                'High': ['mean', 'std', 'min', 'max'],
                'Low': ['mean', 'std', 'min', 'max'],
                'Close': ['mean', 'std', 'min', 'max'],
                'Volume': ['sum', 'mean', 'std']
            }).round(2)
            
            st.dataframe(summary_stats, use_container_width=True)
            
        else:
            st.warning("⚠️ No data found for the selected filters. Please adjust your selection.")
    else:
        st.warning("⚠️ Please select at least one symbol and a valid date range.")
else:
    st.error("❌ No data available. Please upload a CSV file or ensure sample data is present.")

# Footer
st.markdown("---")
st.markdown("**Demo Streamlit App for OHLCV Data Analysis**")
st.markdown("Upload your CSV file with columns: Date, Symbol, Open, High, Low, Close, Volume") 