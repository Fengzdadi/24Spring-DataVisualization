import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import json
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import datetime

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

color_map = {
    'low': 'yellow',    # 0.7 <= Probability < 0.8
    'medium': 'orange', # 0.8 <= Probability < 0.9
    'high': 'red',      # Probability >= 0.9
    'NaN': 'grey'       # NaN值
}

# 读取初始道路数据
with open(
        'D:\\My document\\大学\\大三下\\数据可视化\\24Spring-DataVisualization\\Task2-MapData\\data\\温州交通数据data\\load_track_detail.json',
        'r') as file:
    road_data = json.load(file)
roads_df = pd.DataFrame(road_data)


def generate_base_map(default_location=[28.023353, 120.606054], default_zoom_start=12):
    base_map = folium.Map(location=default_location, control_scale=True, zoom_start=default_zoom_start)
    return base_map

def minutes_to_time(minutes):
    # 计算小时和分钟数
    hours = minutes // 60
    minutes = minutes % 60
    # 格式化为几点几分的形式
    time_str = f"{hours:02d}:{minutes:02d}"
    return time_str


# 应用布局
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dcc.DatePickerSingle(
                    id='date-picker',
                    min_date_allowed=pd.Timestamp('2014-01-01'),
                    max_date_allowed=pd.Timestamp('2014-01-15'),
                    initial_visible_month=pd.Timestamp('2014-01-01'),
                    date=str(pd.Timestamp('2014-01-01')),
                ),
                width=4
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='time-dropdown',
                    options=[{'label': minutes_to_time(i * 5), 'value': i * 5} for i in range(1, 289)],
                    value=5
                ),
                width=4
            ),
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='map-container'), width=12)
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H3('Wenzhou Transportation', style={'text-align': 'center'}),
                    html.Div([
                        html.Div(style={'width': '20px', 'height': '20px', 'background-color': 'red', 'display': 'inline-block'}),
                        html.Span('High congestion', style={'padding-left': '5px'}),
                    ]),
                    html.Div([
                        html.Div(style={'width': '20px', 'height': '20px', 'background-color': 'orange', 'display': 'inline-block'}),
                        html.Span('Moderate congestion', style={'padding-left': '5px'}),
                    ]),
                    html.Div([
                        html.Div(style={'width': '20px', 'height': '20px', 'background-color': 'yellow', 'display': 'inline-block'}),
                        html.Span('Low congestion', style={'padding-left': '5px'}),
                    ]),
                    html.Div([
                        html.Div(style={'width': '20px', 'height': '20px', 'background-color': 'green', 'display': 'inline-block'}),
                        html.Span('Smooth traffic', style={'padding-left': '5px'}),
                    ]),
                ]),
                width=12
            )
        ])
    ])
])


@app.callback(
    Output('map-container', 'children'),
    [Input('date-picker', 'date'),
     Input('time-dropdown', 'value')]
)
def update_output(date, time_minute):
    if date is not None:
        date = pd.Timestamp(date).strftime('%Y%m%d')  # Format date to match filenames
        traffic_filename = f'D:\\My document\\大学\\大三下\\数据可视化\\24Spring-DataVisualization\\Task2-MapData\\data\\温州交通数据data\\five_carflow{date}.json'
        with open(traffic_filename, 'r') as file:
            traffic_data = json.load(file)
        traffic_df = pd.DataFrame(traffic_data)
        traffic_df = traffic_df[traffic_df['time_minute'] == time_minute]

        folium_map = generate_base_map()
        for _, road in roads_df.iterrows():
            road_id = road['id']
            points = []
            for i in range(1, 5):
                lat = road.get(f'lat{i}')
                lng = road.get(f'lng{i}')
                if pd.notna(lat) and pd.notna(lng):
                    points.append((lat, lng))
            # points = [(road[f'lat{i}'], road[f'lng{i}']) for i in range(1, 5) if road[f'lat{i}'] and road[f'lng{i}']]
            if points:
                traffic = traffic_df[traffic_df['road_id'] == road_id]

                car_flow_in = traffic['car_flow_in'].sum()
                color = 'green'        # 'green'
                if car_flow_in > 100:
                    color = 'red'
                elif car_flow_in > 50:
                    color = 'orange'
                elif car_flow_in > 20:
                    color = 'yellow'

                car_flow_out = traffic['car_flow_out'].sum()
                folium.PolyLine(points, color=color, weight=4, opacity=0.7,
                                tooltip=f'Road ID: {road_id}, Car flow in: {car_flow_in}, Car flow out: {car_flow_out}').add_to(folium_map)

        # 保存地图为 HTML 文件并嵌入
        folium_map.save('temp_map.html')
        return html.Iframe(srcDoc=open('temp_map.html', 'r').read(), width='100%', height='800vh')


# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=True)
