import re

# 文件名前缀与日期范围
file_prefix = "five_carflow"
date_start = 20140101
date_end = 20140115

# 遍历日期范围中的每个文件
for date in range(date_start, date_end + 1):
    input_file = f"{file_prefix}{date}.sql"
    output_file = f"{file_prefix}{date}_batch.sql"
    table_name = f"five_carflow{date}"  # 根据文件名动态设置表名

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
            # 使用正则表达式匹配所有 INSERT 语句中的值部分
            inserts = re.findall(r"INSERT INTO `" + table_name + r"` VALUES \((.*?)\);", content)
            # 处理每一组插入数据，去除单引号
            processed_inserts = [
                '(' + re.sub(r"'(\d+)'", r"\1", insert) + ')' for insert in inserts
            ]

        # 如果找到任何插入语句，将其合并成一个批量插入语句
        if processed_inserts:
            bulk_insert_sql = (
                f"INSERT INTO `{table_name}` "
                f"(id, road_id, car_flow_out, car_flow_in, time_minute) VALUES\n" +
                ",\n".join(processed_inserts) + ";"
            )
        else:
            bulk_insert_sql = ""

        # 将批量插入的语句写入新的 .sql 文件中
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("-- 批量插入语句生成\n\n")
            f.write("SET FOREIGN_KEY_CHECKS=0;\n\n")
            f.write(bulk_insert_sql)

        print(f"批量插入的 SQL 语句已保存到 {output_file}")

    except FileNotFoundError:
        print(f"文件 {input_file} 未找到，跳过")
