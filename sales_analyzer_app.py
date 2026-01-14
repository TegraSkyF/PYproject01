import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Sales Data Analyzer",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .anomaly-highlight {
        background-color: #ffebee;
        padding: 0.5rem;
        border-left: 4px solid #f44336;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def detect_anomalies(df, column):
    """
    Detect anomalies in a specified column using IQR method
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    anomalies = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return anomalies

def load_data(uploaded_file):
    """
    Load data from uploaded Excel file
    """
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return None
    return None

def main():
    st.markdown('<h1 class="main-header">📊 Sales Data Analyzer</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select Page", ["Dashboard", "Data Upload", "Anomaly Detection", "Help"])
    
    # Initialize session state
    if 'data' not in st.session_state:
        st.session_state.data = None
    
    if page == "Dashboard":
        dashboard_page()
    elif page == "Data Upload":
        upload_page()
    elif page == "Anomaly Detection":
        anomaly_detection_page()
    elif page == "Help":
        help_page()

def dashboard_page():
    st.header("📈 Dashboard")

    if st.session_state.data is not None:
        df = st.session_state.data

        # Display basic info about the dataset
        st.subheader("Dataset Overview")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(label="Total Records", value=len(df))
        with col2:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                # Assuming the first numeric column is sales
                sales_col = numeric_cols[0]
                total_sales = df[sales_col].sum()
                avg_sales = df[sales_col].mean()
                st.metric(label="Total Sales", value=f"${total_sales:,.2f}", delta=f"Avg: ${avg_sales:,.2f}")
        with col3:
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            st.metric(label="Columns", value=len(df.columns))
        with col4:
            missing_values = df.isnull().sum().sum()
            st.metric(label="Missing Values", value=missing_values)

        # Enhanced Key metrics section
        st.subheader("Key Performance Indicators")

        # Select numeric columns for KPIs
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            # Create columns for metrics
            kpi_cols = st.columns(min(len(numeric_cols), 4))

            for i, col in enumerate(numeric_cols[:4]):
                with kpi_cols[i]:
                    st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
                    st.write(f"**{col.upper()}**")
                    st.write(f"Sum: {df[col].sum():,.2f}")
                    st.write(f"Mean: {df[col].mean():,.2f}")
                    st.write(f"Median: {df[col].median():,.2f}")
                    st.write(f"Std Dev: {df[col].std():,.2f}")
                    st.markdown('</div>', unsafe_allow_html=True)

        # Advanced visualizations section
        st.subheader("Advanced Visualizations")

        # Determine appropriate columns for visualization
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

        # Time series chart if date column exists
        if date_cols and numeric_cols:
            st.subheader("Time Series Analysis")
            date_col = st.selectbox("Select Date Column", options=date_cols, key="time_series_date")
            value_col = st.selectbox("Select Value Column", options=numeric_cols, key="time_series_value")

            if date_col and value_col:
                # Prepare data for time series
                ts_data = df.groupby(date_col)[value_col].sum().reset_index()
                fig_ts = px.line(ts_data, x=date_col, y=value_col, title=f"{value_col} Trend Over Time")
                fig_ts.update_layout(xaxis_title=date_col, yaxis_title=value_col)
                st.plotly_chart(fig_ts, use_container_width=True)

        # Bar chart comparison
        st.subheader("Comparative Analysis")
        if len(numeric_cols) >= 2:
            col1, col2 = st.columns(2)

            with col1:
                bar_x = st.selectbox("Select Category for Bar Chart", options=categorical_cols + numeric_cols[:5], key="bar_x")
            with col2:
                bar_y = st.selectbox("Select Value for Bar Chart", options=numeric_cols, key="bar_y")

            if bar_x and bar_y:
                if bar_x in categorical_cols:
                    bar_data = df.groupby(bar_x)[bar_y].mean().reset_index()
                    fig_bar = px.bar(bar_data, x=bar_x, y=bar_y, title=f"Average {bar_y} by {bar_x}")
                else:
                    # If x-axis is numeric, create bins
                    df['bin'] = pd.cut(df[bar_x], bins=10)
                    bar_data = df.groupby('bin')[bar_y].mean().reset_index()
                    fig_bar = px.bar(bar_data, x='bin', y=bar_y, title=f"Average {bar_y} by {bar_x} Ranges")

                st.plotly_chart(fig_bar, use_container_width=True)

        # Pie chart for distribution
        if categorical_cols:
            st.subheader("Distribution Analysis")
            pie_col = st.selectbox("Select Category for Distribution", options=categorical_cols, key="pie_chart")

            if pie_col:
                pie_data = df[pie_col].value_counts().reset_index()
                pie_data.columns = [pie_col, 'Count']
                fig_pie = px.pie(pie_data, values='Count', names=pie_col, title=f"Distribution of {pie_col}")
                st.plotly_chart(fig_pie, use_container_width=True)

        # Scatter plot for correlation
        if len(numeric_cols) >= 2:
            st.subheader("Correlation Analysis")
            col1, col2 = st.columns(2)

            with col1:
                scatter_x = st.selectbox("Select X-axis for Scatter Plot", options=numeric_cols, key="scatter_x")
            with col2:
                scatter_y = st.selectbox("Select Y-axis for Scatter Plot", options=numeric_cols, key="scatter_y")

            if scatter_x != scatter_y:
                fig_scatter = px.scatter(df, x=scatter_x, y=scatter_y, title=f"{scatter_y} vs {scatter_x}")
                st.plotly_chart(fig_scatter, use_container_width=True)

        # Additional visualizations
        if len(numeric_cols) >= 2:
            st.subheader("Correlation Heatmap")
            corr_df = df[numeric_cols].corr()
            fig_corr = px.imshow(
                corr_df,
                text_auto=True,
                aspect="auto",
                title="Correlation Matrix",
                color_continuous_scale='RdBu',
                range_color=[-1,1]
            )
            st.plotly_chart(fig_corr, use_container_width=True)

        # Histogram for numeric columns
        if numeric_cols:
            st.subheader("Distribution Histograms")
            hist_col = st.selectbox("Select Column for Histogram", options=numeric_cols, key="histogram")
            if hist_col:
                fig_hist = px.histogram(df, x=hist_col, nbins=30, title=f"Distribution of {hist_col}")
                st.plotly_chart(fig_hist, use_container_width=True)

        # Show raw data
        st.subheader("Raw Data Preview")
        st.dataframe(df.head(10))

    else:
        st.info("Please upload a sales data file on the 'Data Upload' page to view the dashboard.")

def upload_page():
    st.header("📁 Data Upload")
    
    st.info("Upload an Excel file (.xlsx) containing your sales data.")
    
    uploaded_file = st.file_uploader(
        "Choose an Excel file", 
        type=["xlsx", "xls"],
        accept_multiple_files=False
    )
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        if df is not None:
            st.success("File uploaded successfully!")
            
            # Display basic info about the uploaded data
            st.subheader("Uploaded Data Preview")
            st.dataframe(df.head())
            
            st.subheader("Data Info")
            buffer = io.StringIO()
            df.info(buf=buffer)
            s = buffer.getvalue()
            st.text(s)
            
            # Store the data in session state
            st.session_state.data = df
            
            st.success("Data loaded and ready for analysis!")
        else:
            st.error("Failed to load the file. Please check the file format.")

def anomaly_detection_page():
    st.header("🔍 Anomaly Detection")

    if st.session_state.data is not None:
        df = st.session_state.data

        st.info("Detecting anomalies in your sales data using statistical methods.")

        # Select column for anomaly detection
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if numeric_cols:
            selected_column = st.selectbox("Select column for anomaly detection", options=numeric_cols)

            if selected_column:
                anomalies = detect_anomalies(df, selected_column)

                st.subheader(f"Anomalies in '{selected_column}' column")

                if not anomalies.empty:
                    st.warning(f"Found {len(anomalies)} anomalies in the data ({(len(anomalies)/len(df)*100):.2f}%)")

                    # Show summary statistics
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric(label="Total Records", value=len(df))
                    with col2:
                        st.metric(label="Anomalies Found", value=len(anomalies))
                    with col3:
                        st.metric(label="Anomaly Rate", value=f"{(len(anomalies)/len(df)*100):.2f}%")
                    with col4:
                        st.metric(label="Mean Value", value=f"{anomalies[selected_column].mean():.2f}")

                    # Display anomalies
                    st.dataframe(anomalies)

                    # Enhanced visualization of anomalies
                    st.subheader("Anomaly Visualization")

                    # Create multiple visualization options
                    viz_option = st.radio(
                        "Select visualization type:",
                        ('Scatter Plot', 'Box Plot', 'Histogram', 'Time Series (if date column exists)')
                    )

                    if viz_option == 'Scatter Plot':
                        fig = go.Figure()

                        # Add normal points
                        normal_data = df[~df.index.isin(anomalies.index)]
                        fig.add_trace(go.Scatter(
                            x=normal_data.index,
                            y=normal_data[selected_column],
                            mode='markers',
                            name='Normal',
                            marker=dict(color='blue', opacity=0.6)
                        ))

                        # Add anomaly points
                        fig.add_trace(go.Scatter(
                            x=anomalies.index,
                            y=anomalies[selected_column],
                            mode='markers',
                            name='Anomaly',
                            marker=dict(color='red', size=10)
                        ))

                        fig.update_layout(
                            title=f"Anomaly Detection for '{selected_column}' - Scatter Plot",
                            xaxis_title="Index",
                            yaxis_title=selected_column
                        )

                        st.plotly_chart(fig, use_container_width=True)

                    elif viz_option == 'Box Plot':
                        # Create a combined box plot
                        fig = go.Figure()

                        fig.add_trace(go.Box(
                            y=df[selected_column],
                            name='All Data',
                            boxmean=True
                        ))

                        if not anomalies.empty:
                            fig.add_trace(go.Box(
                                y=anomalies[selected_column],
                                name='Anomalies',
                                marker_color='red',
                                boxmean=True
                            ))

                        fig.update_layout(
                            title=f"Box Plot Comparison: All Data vs Anomalies",
                            yaxis_title=selected_column
                        )

                        st.plotly_chart(fig, use_container_width=True)

                    elif viz_option == 'Histogram':
                        # Create histogram comparing normal data vs anomalies
                        fig = go.Figure()

                        if len(normal_data) > 0:
                            fig.add_trace(go.Histogram(
                                x=normal_data[selected_column],
                                name='Normal Data',
                                opacity=0.75,
                                marker_color='blue'
                            ))

                        if not anomalies.empty:
                            fig.add_trace(go.Histogram(
                                x=anomalies[selected_column],
                                name='Anomalies',
                                opacity=0.75,
                                marker_color='red'
                            ))

                        fig.update_layout(
                            title=f"Histogram: Normal Data vs Anomalies in '{selected_column}'",
                            xaxis_title=selected_column,
                            yaxis_title="Frequency",
                            barmode="overlay"
                        )

                        st.plotly_chart(fig, use_container_width=True)

                    elif viz_option == 'Time Series (if date column exists)':
                        # Check for date columns to create time series visualization
                        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
                        if date_cols:
                            date_col = st.selectbox("Select Date Column", options=date_cols)

                            # Merge normal and anomaly data with dates
                            df_with_status = df.copy()
                            df_with_status['is_anomaly'] = df_with_status.index.isin(anomalies.index)

                            fig = px.line(
                                df_with_status,
                                x=date_col,
                                y=selected_column,
                                color='is_anomaly',
                                title=f"Time Series with Anomalies Highlighted",
                                color_discrete_map={True: 'red', False: 'blue'}
                            )

                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No date columns found for time series visualization.")

                    # Show detailed statistics
                    st.subheader("Detailed Anomaly Statistics")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Normal Data Statistics**")
                        if len(normal_data) > 0:
                            st.write(f"- Count: {len(normal_data)}")
                            st.write(f"- Mean: {normal_data[selected_column].mean():.2f}")
                            st.write(f"- Std: {normal_data[selected_column].std():.2f}")
                            st.write(f"- Min: {normal_data[selected_column].min():.2f}")
                            st.write(f"- Max: {normal_data[selected_column].max():.2f}")

                    with col2:
                        st.write("**Anomaly Data Statistics**")
                        if not anomalies.empty:
                            st.write(f"- Count: {len(anomalies)}")
                            st.write(f"- Mean: {anomalies[selected_column].mean():.2f}")
                            st.write(f"- Std: {anomalies[selected_column].std():.2f}")
                            st.write(f"- Min: {anomalies[selected_column].min():.2f}")
                            st.write(f"- Max: {anomalies[selected_column].max():.2f}")

                    # Show anomaly values in a table
                    st.subheader("Anomaly Details")
                    anomaly_details = anomalies[[selected_column]].copy()
                    anomaly_details['Index'] = anomaly_details.index
                    anomaly_details = anomaly_details.reset_index(drop=True)
                    anomaly_details = anomaly_details[['Index', selected_column]]
                    anomaly_details.columns = ['Original Index', selected_column]
                    st.dataframe(anomaly_details)

                else:
                    st.success(f"No anomalies detected in '{selected_column}' column using IQR method.")

                    # Still show some visualizations for the selected column
                    st.subheader(f"Analysis of '{selected_column}' (No Anomalies Detected)")

                    col1, col2 = st.columns(2)

                    with col1:
                        fig_hist = px.histogram(df, x=selected_column, nbins=30, title=f"Distribution of {selected_column}")
                        st.plotly_chart(fig_hist, use_container_width=True)

                    with col2:
                        fig_box = px.box(df, y=selected_column, title=f"Box Plot of {selected_column}")
                        st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.warning("No numeric columns found in the dataset for anomaly detection.")
    else:
        st.info("Please upload a sales data file first on the 'Data Upload' page.")

def help_page():
    st.header("ℹ️ Help & Documentation")
    
    st.markdown("""
    ## 📊 Sales Data Analyzer - Help Guide
    
    Welcome to the Sales Data Analyzer! This application helps you analyze sales data with key metrics, visualizations, and anomaly detection.
    
    ### 📁 Supported File Format
    
    The application accepts Excel files with the following characteristics:
    
    - **File Extension**: `.xlsx` or `.xls`
    - **Structure**: Tabular data with rows and columns
    - **Recommended Columns** (but not required):
        - Date/Time column (for time series analysis)
        - Numeric columns (for sales figures, quantities, prices, etc.)
        - Categorical columns (for products, regions, categories, etc.)
    
    ### 🚀 How to Use the Application
    
    1. **Data Upload**:
        - Navigate to the "Data Upload" page
        - Click "Browse files" and select your Excel file
        - Wait for the data to load and preview
    
    2. **Dashboard**:
        - View key metrics and visualizations
        - Select different columns to visualize relationships
        - Explore correlations between variables
    
    3. **Anomaly Detection**:
        - Select a numeric column to analyze
        - The system will identify outliers using statistical methods
        - View anomalous records and their visualization
    
    4. **Help**:
        - Access this help page anytime
    
    ### 🔍 Anomaly Detection Method
    
    The application uses the Interquartile Range (IQR) method to detect anomalies:
    - Calculate Q1 (25th percentile) and Q3 (75th percentile)
    - Compute IQR = Q3 - Q1
    - Define bounds: Lower = Q1 - 1.5×IQR, Upper = Q3 + 1.5×IQR
    - Values outside these bounds are considered anomalies
    
    ### 💡 Tips
    
    - Ensure your Excel file contains clean, organized data
    - Remove any summary rows or headers that aren't part of the data
    - Numeric columns work best for analysis and visualization
    - Check for missing values which might affect analysis
    
    ### ❗ Troubleshooting
    
    If you encounter issues:
    - Verify the file is a valid Excel file (.xlsx or .xls)
    - Check that the file isn't password protected
    - Ensure the file size isn't too large (recommended < 100MB)
    - Make sure the file contains tabular data
    
    For additional support, contact your system administrator.
    """)
    
    st.divider()
    
    st.subheader("📋 Sample Data Format")
    
    st.markdown("""
    Here's an example of how your data should be structured:
    
    | Date       | Product    | Region | Sales | Quantity | Price |
    |------------|------------|--------|-------|----------|-------|
    | 2023-01-01 | Product A  | North  | 1000  | 10       | 100   |
    | 2023-01-02 | Product B  | South  | 1500  | 15       | 100   |
    | 2023-01-03 | Product C  | East   | 2000  | 20       | 100   |
    
    Note: Column names and types can vary based on your specific data.
    """)

if __name__ == "__main__":
    main()