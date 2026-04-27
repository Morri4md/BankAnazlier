# Bank Statement Analyzer

## Overview

This script takes a bank statement exported as a CSV file and automatically processes the transaction data to generate a structured spending report. It cleans inconsistent transaction descriptions, extracts merchant names, identifies locations from transaction text, and groups spending totals by merchant.

The program is designed to handle real-world financial data, which is often messy and inconsistent, especially when transactions include extra formatting such as Apple Pay tags, store codes, or combined merchant and location strings.

## Input Format / Tips

CSV has to be in a date,description, amount format (Example: 04/20/2026,CHICK-FIL-A WEST CHESTER OH,25.60)
There are csv's provided named Report1.csv all the way up to Report5.csv in the correct formating

## Why This Script Is Useful

Bank statements from financial institutions are not always easy to analyze manually because they contain unstructured and inconsistent descriptions. This script automates the process of organizing that data, which makes it easier to understand spending habits without manually sorting through each transaction.

It is useful for:
- Tracking personal spending patterns
- Quickly identifying where money is being spent most frequently
- Cleaning and standardizing messy financial data
- Saving time compared to manual spreadsheet analysis
- Providing a simple way to summarize financial activity from raw CSV exports

By automating categorization and summarization, the script turns raw transaction data into meaningful insights that can help users make better financial decisions.