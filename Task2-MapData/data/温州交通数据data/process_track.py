import re
import json


def convert_sql_to_json(input_filename, output_filename):
    # 读取 SQL 文件内容
    with open(input_filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式提取表字段名称
    create_table_pattern = re.compile(r"CREATE TABLE `load_track_detail` \((.*?)\),", re.S)
    create_table_content = re.search(create_table_pattern, content)
    if not create_table_content:
        print(f"No table creation statement found in {input_filename}")
        return

    # 获取列名
    columns = re.findall(r"`(.*?)`", create_table_content.group(1))

    # 使用正则表达式提取所有值
    values_pattern = re.compile(r"INSERT INTO `load_track_detail` VALUES \((.*?)\);", re.S)
    values = values_pattern.findall(content)

    # 将提取的值转换为字典列表
    data_list = []
    for value in values:
        row_values = value.split(", ")
        # 格式化行值，处理 'null' 和 数字类型
        formatted_row = [
            None if val.strip().lower() == 'null' else float(val.strip("'")) if '.' in val else int(val.strip("'"))
            for val in row_values
        ]
        data_dict = {column: val for column, val in zip(columns, formatted_row)}
        data_list.append(data_dict)

    # 将字典列表转换为 JSON 并保存到文件
    with open(output_filename, 'w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, indent=4)

    print(f"JSON file '{output_filename}' has been created.")


# 调用函数，将 `load_track_detail.sql` 转换为 JSON 文件
convert_sql_to_json("load_track_detail.sql", "load_track_detail.json")
