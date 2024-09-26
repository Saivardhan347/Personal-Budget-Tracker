import budget_tracker as bt
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import tabulate as tabl
import sys

home_options = {1:"Income", 2:"Budgets", 3:"Expenses", 4:"View Summery", 5:"Reset Data", 6:"Close Budget Tracker"}

def welcome():
    print("\n________________________Welcome to Budget Tracker______________________")

def back():
    print("\nBack to home : y/n")
    bto = str(input("Select y/n : "))
    if bto == "y":
        options()
    elif bto == "n":
        sys.exit()
   
def income():
    print("\n--------------------------------Income-------------------------------\n")
    print("1.Show Income \n2.Add income \n3.Back to home")
    income_val = int(input("Enter the value of choosen option : "))
    if income_val == 1:
        year = int(input("Enter the year in yyyy format : "))
        tracker = bt.BudgetTracker(year)
        tracker.load_data()
        print(f"--------------------Monthly income of {year}-------------------------")
        for i in tracker.income:
            print(f"{i} : {tracker.income[i]}")
        print(f"\nTotal income of {year} = {sum(tracker.income.values())}")
        print(f"Balance Amount of {year} = {round(tracker.month_df().iloc[-1,-1],2)}")
        tracker.save_data()
        income()
    elif income_val == 2:
        income_date = input("Enter the date in  dd-mm-yyyy format : ")
        income_amount = float(input("Enter the income : "))
        tracker = bt.choose_obj(income_date)
        tracker.load_data()
        tracker.add_income(income_date, income_amount)
        tracker.save_data()
        income()
    elif income_val == 3:
        options()
                 
def budgets():
    print("\n--------------------------------Budgets-------------------------------\n")
    print("1.Set Budget \n2.Show budgets \n3.Change Budget \n4.Back to home")
    budget_selection = int(input("Enter the value of choosen option : "))
    if budget_selection == 1:
        budget_year = int(input("Enter the year in yyyy format : "))
        budget_month = input("Enter the Month Full Name : ")
        budget_amount = float(input("Enter Budget amount : "))
        tracker = bt.BudgetTracker(budget_year)
        tracker.load_data()
        tracker.set_budget(budget_month, budget_amount)
        print(f"Budget set for {budget_month, budget_year} : {budget_amount}")
        tracker.save_data()
        budgets()
    elif budget_selection == 2:
        print()
        year = int(input("Enter the year in yyyy format : "))
        tracker = bt.BudgetTracker(year)
        tracker.load_data()
        print(f"--------------------Monthly budget of {year}-------------------------")
        for i in tracker.budget:
            print(f"{i} : {tracker.budget[i]}")
        budgets()
    elif budget_selection == 3:
        year = int(input("Enter the year in yyyy format : "))
        tracker = bt.BudgetTracker(year)
        tracker.load_data()
        for i in tracker.budget:
            print(f"{i} : {tracker.budget[i]}")
        change_month = str(input("Enter the month to change : "))
        change_amount = float(input("Enter Budget amount : "))
        tracker.set_budget(change_month, change_amount)
        print(f"Budget for {change_month, year} is successfully changed to {change_amount}.")
        tracker.save_data()
        budgets()
    elif budget_selection == 4:
        options()
        
def expenses():
    print("\n--------------------------------Expenses-------------------------------\n")
    print("Total expenses = ")
    print("1.Add Expenses \n2.Show expenses \n3.Delete Expense \n4.Back to home")
    expenses_selection = int(input("Enter the value of choosen option : "))
    if expenses_selection == 1:
        date = input("Enter the date in  dd-mm-yyyy format : ")
        tracker = bt.choose_obj(date)
        tracker.load_data()
        category = tracker.default_category
        print("Select the category for adding the Expenses")
        for q in range(len(category)):
            print(f"{q+1} : {category[q]}")
            
        category_option = int(input("Enter the value of choosen category : "))
        for r in range(len(category)):
            if category_option < len(category) and r == category_option:
                selected_category = category[r-1]
                print(selected_category)
                break
            elif category_option == len(category):
                custom_category = str(input(("Enter custom category : ")))
                category.insert(-1, custom_category)
                selected_category = custom_category
                print(selected_category)
        
        expenses_amount = float(input("Enter expense amount : "))
        notes = input("Enter Expense description : ")
        tracker.add_expense(date, selected_category, expenses_amount, notes)
        tracker.save_data()
        expenses()
    elif expenses_selection == 2:
        print()
        year = int(input("Enter the year in yyyy format : "))
        tracker = bt.BudgetTracker(year)
        tracker.load_data()
        data ={
            "Date" : tracker.date,
            "Category": tracker.category,
            "Expenses": tracker.expenses,
            "Notes": tracker.notes
        }
        print(pd.DataFrame(data).to_string(index=False))
        expenses()
    elif expenses_selection == 3:
        year = int(input("Enter the year in yyyy format : "))
        tracker = bt.BudgetTracker(year)
        tracker.load_data()
        df = tracker.daily_df()
        print(df.to_string())
        delete_row = int(input("Enter the row number to delete : "))
        print(f"Expenses on {df.loc[delete_row,"Date"]}_{df.loc[delete_row,"Category"]} is successfully deleted.")
        df.drop(index=delete_row, inplace=True)
        tracker.date = list(df["Date"])
        tracker.category = list(df["Category"])
        tracker.expenses = list(df["Expenses"])
        tracker.notes = list(df["Notes"])
        tracker.save_data()
        expenses()
    elif expenses_selection == 4:
        options()
                  
def view_summery():
    print("\n--------------------------------Summery-------------------------------\n")
    directory = Path.cwd()/"Excel Sheets"
    years_list = []
    for file_path in directory.iterdir():
        year = int(file_path.name[0:4])
        if year not in years_list:
            years_list.append(year)

    for i in range(len(years_list)):
        print(f"{i+1} : {years_list[i]}")
    year = int(input("Enter the year to see the summery : "))
    tracker = bt.BudgetTracker(year)
    tracker.load_data()
    daily_df = tracker.daily_df()
    monthly_df = tracker.month_df()
    print("\n------------------------Expenses Data-------------------------\n")
    print(daily_df)
    print("\n-------------------------Monthly Summery-----------------------\n")
    print(monthly_df)
    tracker.save_data()

    print(f"\n--------------------------{year} Monthly Expenses-----------------------------\n")
    month_list = list(monthly_df.columns[i] for i in range(1,len(monthly_df.columns)-1))
    expenses_months = list(monthly_df.iloc[-2,1:len(monthly_df.columns)-1])
    plt.figure(figsize=(25,10))
    plt.bar(month_list,expenses_months, width=0.4)
    plt.grid(axis="y", ls="dashed")
    plt.title(f"{year} Monthly Expenses")
    plt.xlabel("Month")
    plt.ylabel("Expense amount")
    plt.show()
    
    print(f"\n--------------------------{year} Expenses of Categories-----------------------------\n")
    category = list(monthly_df.loc[2:len(monthly_df)-3,"Category"])
    expense = list(monthly_df.loc[2:len(monthly_df)-3,"Category Total_Year"])
    
    plt.figure(figsize=(25,10))
    plt.bar(category,expense, width=0.4)
    plt.grid(axis="y", ls="dashed")
    plt.title(f"{year} Expenses of Categories")
    plt.xlabel("Categories")
    plt.ylabel("Expense amount")
    plt.ylim(0,70000)
    plt.show()
    
    print("Enter the month to know the month expenses of the categories")
    month = input("month full name : ")
    month_expense = list(monthly_df.loc[2:len(monthly_df)-3,month])
    print(f"\n--------------------------{month} Expenses of Categories-----------------------------\n")
    data = {
        "Category":category,
        "Expense Amount" : month_expense
    }
    table = tabl.tabulate(data, headers="keys", tablefmt="grid")
    print(table)
    
    plt.figure(figsize=(25,10))
    plt.bar(category,month_expense, width=0.4)
    plt.grid(axis="y", ls="dashed")
    plt.title(f"{month} Expenses of Categories")
    plt.xlabel("Categories")
    plt.ylabel("Expense amount")
    plt.show()
    options()
    print()
    
    
        
    
def options():
    print("\n--------------------------------Home-------------------------------\n")
    for p in home_options:
        print(f"{p} : {home_options[p]}")
    selected_option = int(input("Enter the value of choosen option : "))
    if selected_option == 1:
        income()
    elif selected_option == 2:
        budgets()
    elif selected_option == 3:
        expenses()
    elif selected_option == 4:
        view_summery()
    elif selected_option == 5:
        bt.reset()
    elif selected_option == 6:
        sys.exit()
