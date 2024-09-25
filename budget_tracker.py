import pandas as pd
from pathlib import Path
import sys
import datetime as dt
import calendar
 
new_dirc = Path.cwd() / "Excel Sheets"
try:
    new_dirc.mkdir(exist_ok = False)
except FileExistsError:
    pass

class BudgetTracker:
    def __init__(self,year):
        self.y = year
        self.income = {}
        self.budget = {}
        self.default_category=[]
        self.date = []
        self.category = []
        self.expenses = []
        self.notes = []
        self.filename = f"{self.y}_Budget_Tracker_data.xlsx"
        self.filepath = Path.cwd()/"Excel Sheets"/self.filename
                    
    def add_income(self,date, amount):
        month = pd.to_datetime(date, dayfirst=True).strftime("%B")
        if month in self.income.keys():
            self.income[month] += amount
        else:
            self.income[month] = amount   
        print(f"\nIncome added: {amount}")

    def add_expense(self,date, category, amount,notes="-"):        
        self.date.append(date)
        self.category.append(category)
        self.expenses.append(amount)
        self.notes.append(notes)
        print(f"Expense added to {category} : {amount}")
    
    def set_budget(self, month, amount):
        self.budget[month] = amount
        
    def daily_df(self):
        daily_data = {
            "Date" : self.date,
            "Category": self.category,
            "Expenses": self.expenses,
            "Notes": self.notes
            }
        daily_df = pd.DataFrame(daily_data)
        return daily_df
        
    def month_df(self):
        daily_data = {
            "Date" : self.date,
            "Category": self.category,
            "Expenses": self.expenses,
            "Notes": self.notes
            }
        daily_df = pd.DataFrame(daily_data)
        
        conv_date_list = list(pd.to_datetime(self.date, dayfirst=True))
        
        month_list  = []
        for i in conv_date_list:
            month = i.strftime("%B")
            if month not in month_list:
                month_list.append(month)
                
        month_list = list(set(month_list + list(self.income.keys()) + list(self.budget.keys())))
        months_order = {month : index for index,month in enumerate(calendar.month_name)  if month}
        f_month_list = sorted(month_list, key = lambda month: months_order[month])
        category = ["Income", "Budget"] + sorted(list(set(self.category)))
        
        keys = ["Category"] + f_month_list
        values = [category] + [[0.0 for i in range(len(category))] for i in range(1,len(keys))]

        monthly_data = dict(zip(keys,values))
        monthly_df = pd.DataFrame(monthly_data)
        
        for month,amount in self.income.items():
            monthly_df.loc[0,[month]] += amount
        
        for month,amount in self.budget.items():
            monthly_df.loc[1,[month]] += amount
        
        for i in range(len(daily_df)):
            month = conv_date_list[i].strftime("%B")
            category = str(daily_df.loc[i,"Category"])
            expense = float(daily_df.loc[i, "Expenses"])
            monthly_df.loc[monthly_df["Category"]==category,[month]] += expense
        
        expenses_sum = monthly_df.iloc[2:,1:].sum()
        monthly_df.loc[len(monthly_df)] = ["Month Expenses"] + list(expenses_sum)
        
        balance = monthly_df.iloc[0, 1:] - monthly_df.iloc[len(monthly_df)-1,1:]
        monthly_df.loc[len(monthly_df)] = ["Balance Amount"] + list(balance)
        
        monthly_df["Category Total_Year"] = 0
        monthly_df["Category Total_Year"] = monthly_df.iloc[:,1:].sum(axis=1)
        return monthly_df
    
    def save_data(self):       
        daily_df = self.daily_df()
        monthly_df = self.month_df()

        with pd.ExcelWriter(self.filepath, engine="openpyxl") as writer:
            daily_df.to_excel(writer, sheet_name="Daily_Expense", index=False)
            monthly_df.to_excel(writer, sheet_name="Monthly_Expense", index=False)
        print(f"Data saved to {self.filename}")

    def load_data(self):
        try:           
            daily_data = pd.read_excel(self.filepath, sheet_name="Daily_Expense")
            daily_df = pd.DataFrame(daily_data)
            monthly_data = pd.read_excel(self.filepath, sheet_name="Monthly_Expense")
            monthly_df = pd.DataFrame(monthly_data)
            
            income = dict(monthly_df.iloc[0,1:len(monthly_df.columns)-1])
            income_val = [float(i) for i in income.values()]
            self.income = dict(zip(income.keys(),income_val))
            
            budget = dict(monthly_df.iloc[1,1:len(monthly_df.columns)-1])
            budget_val = [float(i) for i in budget.values()]
            self.budget = dict(zip(budget.keys(),budget_val))
            
            category1 = list(monthly_df.loc[2:len(monthly_df)-2,"Category"])
            category2 = ["Investment", "Savings", "Home-Bills", "Groceries", "Vehicle Expense", "Travel","Food and drinks", "Shopping"]
            self.default_category = sorted(list(set(category1 + category2))) + ["Custom"]
            
            self.date = list(daily_df["Date"])
            self.category = list(daily_df["Category"])
            self.expenses = list(daily_df["Expenses"])
            self.notes = list(daily_df["Notes"])
                
            print(f"Data loaded from {self.filename}")
        except FileNotFoundError:
            print(f"No data file found with name {self.filename}")
            
def reset():
    directory = Path.cwd()/"Excel Sheets"
    for file_path in directory.iterdir():
        file_path.unlink()
    print("Budget Tracker has been successfully reset. All data have been cleared.")
    sys.exit()

def choose_obj(date):
    y = pd.to_datetime(date, dayfirst=True).strftime("%Y")
    return BudgetTracker(y)
