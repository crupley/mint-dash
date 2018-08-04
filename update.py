#!/usr/bin/env python3

import sqlite3
import numpy as np
import pandas as pd

# Updates transactions database when transactions.csv has been changed

# mapping from master category to sub-category
mc = {
  "Housing": ["Home", "Home Improvement", "Home Insurance", "Home Services", "Home Supplies", "Lawn & Garden", "Mortgage & Rent"],
  "Food": ["Fast Food", "Food & Dining", "Groceries", "Restaurants"],
  "Bills": ["Bills & Utilities", "Home Phone", "Internet", "Mobile Phone", "Student Loan", "Television", "Utilities", "Web Hosting"],
  "Health": ["Dentist", "Doctor", "Eyecare", "Gym", "Hair", "Health & Fitness", "Health Insurance", "Personal Care", "Pharmacy"],
  "Travel": ["Air Travel", "Hotel", "Travel", "Vacation"],
  "Transport": ["Auto & Transport", "Auto Insurance", "Auto Payment", "Gas & Fuel", "Parking", "Public Transportation", "Registration", "Rental Car & Taxi", "Service & Parts"],
  "Entertainment": ["Amusement", "Alcohol & Bars", "Arts", "Coffee Shops", "Entertainment", "Movies & DVDs", "Music", "Newspapers & Magazines", "Spa & Massage", "Sports"],
  "Stuff": ["Books", "Books & Supplies", "Clothing", "Electronics & Software", "Furnishings", "Hobbies", "Office Supplies", "Pet Food & Supplies", "Printing", "Shopping", "Sporting Goods"],
  "Other": ["Advertising", "ATM Fee", "Bank Fee", "Business Services", "Charity", "Check", "Education", "Federal Tax", "Fees & Charges", "Finance Charge", "Financial", "Gift", "Gifts & Donations", "Late Fee", "Local Tax", "Moving Expenses", "Personal Development", "Pets", "Service Fee", "Shipping", "State Tax", "Taxes", "Trade Commissions", "Uncategorized", "Wedding", "Work Reimbursable"],
  "Ignore": ["Cash & ATM", "Credit Card Payment", "Hide from Budgets & Trends", "Investments", "Kids", "Savings", "Transfer", "Transfer for Cash Spending", "Transfer to Savings"],
  "Income": ["Bonus", "Income", "Interest Income", "Paycheck", "Rental"]
}

mc_reverse = {v:k for k in mc for v in mc[k]}

def prepareData():
    df = pd.read_csv('data/transactions.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['year'] = df['Date'].apply(lambda x: x.year)
    df['month'] = df['Date'].apply(lambda x: x.month)
    df['day'] = df['Date'].apply(lambda x: x.day)
    df['master_category'] = df['Category'].replace(mc_reverse)
    df.columns = [c.replace(' ', '_').lower() for c in df.columns]
    return df


def run():
    df = prepareData()

    # create transactions table, replace if exists
    conn = sqlite3.connect('data/transactions.db')
    df.to_sql('transactions', conn, index=None, if_exists='replace')
    conn.close()




if __name__ == '__main__':
    run()