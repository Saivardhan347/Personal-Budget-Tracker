# Personal Budget Tracker

A Python-based application to track income, manage expenses, and generate structured financial summaries using Excel automation.

This project demonstrates practical financial data processing, structured reporting, and automation using Python and Pandas.

---

## 📌 Problem Statement

Managing personal finances manually in spreadsheets can be inconsistent and time-consuming. Users often struggle to:

- Track categorized expenses  
- Monitor monthly spending trends  
- Maintain structured financial records  
- Generate summary reports efficiently  

This application automates expense tracking and reporting using structured Excel-based workflows.

---

## 🚀 Key Features

- Add income and expense entries  
- Categorize transactions (Rent, Food, Travel, Utilities, etc.)  
- Read structured expense data from Excel files  
- Automatically generate updated financial reports  
- Maintain persistent financial records  
- Simple console-based user interface for interaction  
- Export processed data into Excel format for further analysis  

---

## 🛠 Tech Stack

- Python  
- Pandas  
- Excel File Handling (read/write automation)  
- Console-based UI interaction  
- File I/O operations  

---

## 📂 Project Structure

personal-budget-tracker/
│
├── budget_tracker.py      # Contains the BudgetTracker class
├── UI.py                  # Handles user input and output
├── main.py                # Main script to run the app
├── Excel_sheets/          # Folder where Excel sheets are stored
├── requirements.txt       # Required Libraries
└── README.md              # Project documentation


- `main.py` → Entry point of the application  
- `budget_tracker.py` → Core logic and data handling  
- `UI.py` → User interaction and input handling  

1. **`budget_tracker.py`**:
   - Contains the `BudgetTracker` class.
   - Methods include:
     - `add_income()`: Add income for specific months.
     - `set_budget()`: Set monthly budgets.
     - `add_expense()`: Add expenses with details such as date, category, and notes.
     - `save_data()`: Save the budget and expense data in Excel sheets.
     - `load_data()`: Load data from existing Excel sheets.
   
2. **`UI.py`**:
   - Handles user interaction by taking input and displaying outputs.
   
3. **`main.py`**:
   - Main file to initialize and run the entire application.
---

## ▶️ How to Run Locally

1. Clone the Repository

   ```bash
   git clone https://github.com/Saivardhan347/Personal-Budget-Tracker.git
   cd Personal-Budget-Tracker

2. pip install -r requirements.txt

3. python main.py


## Future Enhancements

Data visualization dashboards (monthly trends, category-wise spending).
Database integration (SQLite / MySQL).
A web interface using Flask or Streamlit.
Predictive expense forecasting.