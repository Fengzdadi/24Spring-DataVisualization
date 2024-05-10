import re
import json

def convert_sql_to_json(input_filename, output_filename, table_name):
    """ 将 SQL 文件转换为 JSON 文件 """
    # 读取 SQL 文件
    with open(input_filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式提取列名
    pattern = re.compile(rf"INSERT INTO `{table_name}` \((.*?)\) VALUES")
    columns_match = re.search(pattern, content)
    if not columns_match:
        print(f"No columns found in {input_filename}")
        return

    # 获取列名
    columns = columns_match.group(1).split(", ")

    # 提取所有值，过滤掉单引号
    values = re.findall(r"\(([\d, ]+)\)", content)

    # 将提取的值转换为字典列表
    data_list = []
    for value in values:
        row_values = value.split(", ")
        data_dict = {column: int(row_value) for column, row_value in zip(columns, row_values)}
        data_list.append(data_dict)

    # 将字典列表转换为 JSON 并保存到文件
    with open(output_filename, 'w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, indent=4)

    print(f"JSON file '{output_filename}' has been created.")

# 循环转换20140101到20140115的文件
start_date = 20140101
end_date = 20140115

for date in range(start_date, end_date + 1):
    sql_filename = f"five_carflow{date}_batch.sql"
    json_filename = f"five_carflow{date}.json"
    table_name = f"five_carflow{date}"
    convert_sql_to_json(sql_filename, json_filename, table_name)
