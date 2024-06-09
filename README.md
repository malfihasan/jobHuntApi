# 📊 jobHuntApi
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.12.0-brightgreen)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-1.4.2-orange)](https://pandas.pydata.org/)

An API to help folks curate job search lists from Fortune 500 and S&P 500 companies.

## 📂 Data
1. **Fortune 500 Companies**: 
   - Download the list of Fortune 500 companies along with their ticker symbols from any reputable website.
   - Also a helping repo can be found in this [link](https://github.com/malfihasan/prjFortune500Scrapper)

2. **S&P 500 Companies**:
   - Download the list of S&P 500 companies along with their ticker symbols from any reputable website.

3. **Private Companies**:
   - For a list of private companies, you can refer to this [Wikipedia link](https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue).

## 🚀 Streamlit App
To run the Streamlit application, follow the steps below:

### 1. Clone the Repository
```sh
git clone https://github.com/malfihasan/jobHuntApi.git
cd jobHuntApi
```

### 2. Install Dependencies
We use [Poetry](https://python-poetry.org/) for dependency management. Ensure you have Poetry installed, then run:
```sh
poetry install
```

### 3. Run the Application
Start the Streamlit app with the following command:
```sh
poetry run streamlit run main.py
```

## 📝 Project Structure
The project is organized as follows:
```
jobHuntApi/
├── data/
│   ├── fortune_500.csv
│   ├── sp_500.csv
│   └── private_companies.csv
├── src/
│   ├── settings.py
│   ├── lib_common.py
│   ├── company_screen.py
│   └── main.py
├── README.md
├── pyproject.toml
└── poetry.lock
```

## 📋 Application Details

### Main Page (`main.py`)
- **Page Title**: The title is set to "Job Search Tool" with an appropriate emoji and a wide layout.
- **Sidebar**: Contains a logo, a title, and a menu for navigating between different screens.
- **Main Content**: Connects to different screens based on the selected menu item.

### Company Screen (`company_screen.py`)
- **Company Screener**: Displays all company data in a detailed table.
- **Company Selection Criteria**: Lists criteria for selecting companies (e.g., revenue, profits, market cap, and halal status).
- **Filtered Companies**: Displays companies that meet the selection criteria.
- **Filtered Tech Companies**: Specifically filters and displays tech companies from the selected companies.

### Utility Functions
- `load_css()`: Loads custom CSS for styling.
- `process_df()`: Processes the DataFrame for use in the app.
- `get_csv()`: Reads a CSV file.
- `csv_save()`: Saves a DataFrame to a CSV file.
- `display_top_companies()`: Displays top companies based on a specified metric.

## 📋 Requirements 
All necessary dependencies are listed in the `pyproject.toml` file. To install them, use the following command:
```sh
poetry install
```

For further assistance or questions, feel free to open an issue or contact 'mdalfihasan19@gmail.com' or put a PR.

Enjoy using the Job Hunt API! 🎉
