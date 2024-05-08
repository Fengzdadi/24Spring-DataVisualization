import json
import pandas as pd
import folium

# 加载道路数据
with open('D:\\My document\\大学\\大三下\\数据可视化\\24Spring-DataVisualization\\Task2-MapData\\data\\温州交通数据data\\load_track_detail.json', 'r') as file:
    road_data = json.load(file)

# 转换道路数据为 DataFrame
df_roads = pd.DataFrame(road_data)

# 函数：加载并处理交通流量数据
def load_traffic_data(date):
    filename = f'D:\\My document\\大学\\大三下\\数据可视化\\24Spring-DataVisualization\\Task2-MapData\\data\\温州交通数据data\\five_carflow{date}.json'
    with open(filename, 'r') as file:
        traffic_data = json.load(file)
    return pd.DataFrame(traffic_data)

# 初始化地图
def init_map(lat, lng):
    return folium.Map(location=[lat, lng], zoom_start=13)

# 添加道路到地图
def add_roads_to_map(map_obj, df_roads, df_traffic):
    for idx, row in df_roads.iterrows():
        points = []
        # 确保所有的点都是有效的，跳过 NaN 值
        for i in range(1, 5):
            lat = row.get(f'lat{i}')
            lng = row.get(f'lng{i}')
            # 添加检查以确保 lat 和 lng 都不是 NaN
            if pd.notna(lat) and pd.notna(lng):
                points.append((lat, lng))

        # 如果存在有效的坐标点则绘制线段
        if points:
            road_id = row['id']
            traffic_info = df_traffic[df_traffic['road_id'] == road_id]
            # 获取当前路段的最大出车流量，如果不存在则标记 "No data"
            car_flow_out = traffic_info['car_flow_out'].max() if not traffic_info.empty else 'No data'
            # 在地图上绘制多段线并附加提示信息
            folium.PolyLine(
                points,
                color='blue',
                tooltip=f'Road ID: {road_id}, Car flow out: {car_flow_out}'
            ).add_to(map_obj)



# 选择日期和时间（示例：20140101 和 time_minute 为 15）
selected_date = '20140101'
selected_time = 15
df_traffic = load_traffic_data(selected_date)
df_traffic = df_traffic[df_traffic['time_minute'] == selected_time]  # 筛选特定时间

# 初始化地图
map_obj = init_map(28.02335324931708, 120.60605406761171)
add_roads_to_map(map_obj, df_roads, df_traffic)

# 保存地图
map_obj.save('Traffic_Map.html')
