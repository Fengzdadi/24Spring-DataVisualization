import pandas as pd
import os

def preprocess_data(file_path):
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('[$,()]', '')
    data = data.loc[:, ~data.columns.duplicated()]
    money_columns = [col for col in data.columns if 'gross' in col or 'budget' in col]
    for col in money_columns:
        data[col] = pd.to_numeric(data[col].replace('[\$,]', '', regex=True), errors='coerce')
    return data

def save_data_to_json(data, output_filename):
    # 将 DataFrame 保存为 JSON 文件
    data.to_json(output_filename, orient='records', lines=True)

def process_files(directory, start_year, end_year):
    for year in range(start_year, end_year + 1):
        file_name = f"Most Profitable Hollywood Stories - US {year}.csv"
        file_path = os.path.join(directory, file_name)
        json_output_path = os.path.join(directory, f"{year}_data.json")  # 定义每个年份的 JSON 输出路径
        if os.path.exists(file_path):
            print(f"Processing file: {file_path}")
            yearly_data = preprocess_data(file_path)
            save_data_to_json(yearly_data, json_output_path)  # 保存该年份的数据到 JSON
            print(f"Data for {year} saved to {json_output_path}")
        else:
            print(f"File not found: {file_path}")

# 示例调用
directory = r'D:\My document\大学\大三下\数据可视化\24Spring-DataVisualization\Task3-Hollywood\好莱坞电影数据集\Hollywood Movie Dataset'
start_year = 2007
end_year = 2011

process_files(directory, start_year, end_year)
