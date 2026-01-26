@echo off
REM Script to start the Sales Data Analyzer application

echo Starting Sales Data Analyzer...
echo Please make sure you have the sales_data.xlsx file in this directory.
echo The application will be accessible at http://localhost:8501

REM Activate virtual environment and start the application
call venv\Scripts\activate.bat
streamlit run sales_analyzer_app.py

pause