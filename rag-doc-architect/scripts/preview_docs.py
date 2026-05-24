import os
import pandas as pd
import openpyxl

folder = r'C:\Users\michael\Desktop\拆开新增财经部-财经经理-出纳'
files_to_check = [
    '出纳-职位说明书.xlsx',
    '财务经理财管方向-职位说明书.xlsx',
    '出纳-八爪鱼图.xlsx',
    '财务经理财管方向-八爪鱼图.xlsx',
    '出纳-任职资格.xlsx',
    '财务经理财管方向-任职资格.xlsx'
]

print("=== Starting Preview of Document Structures ===")
for f in files_to_check:
    path = os.path.join(folder, f)
    if not os.path.exists(path):
        print(f"File not found: {f}")
        continue
        
    print(f"\n>>>> File: {f} <<<<")
    try:
        excel = pd.ExcelFile(path)
        for sheet_name in excel.sheet_names:
            print(f"  --- Sheet: {sheet_name} ---")
            df = pd.read_excel(path, sheet_name=sheet_name, header=None)
            print(df.head(15).to_string())
    except Exception as e:
        print(f"Error parsing {f}: {e}")

print("\n=== Done ===")
