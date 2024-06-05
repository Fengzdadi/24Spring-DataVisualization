import pandas as pd
import os
import networkx as nx
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go


# 读取数据
def load_data(directory, start_year, end_year):
    all_data = []
    for year in range(start_year, end_year + 1):
        file_path = os.path.join(directory, f"{year}_data.json")
        print(f"Checking file: {file_path}")  # 检查文件路径
        if os.path.exists(file_path):
            try:
                yearly_data = pd.read_json(file_path, lines=True)
                yearly_data['Year'] = year
                print(f"Loaded data for {year}: {yearly_data.shape[0]} rows")  # 打印每年加载的数据行数
                all_data.append(yearly_data)
            except ValueError as e:
                print(f"Error reading {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")

    if all_data:
        data = pd.concat(all_data, ignore_index=True)
        data.columns = data.columns.str.strip().str.replace(" ", "_").str.lower()
        print("Columns in loaded data:", data.columns.tolist())  # 打印列名
        print(f"Total loaded data: {data.shape[0]} rows")  # 打印总的数据行数
        return data
    else:
        print("No data loaded.")
        return None  # 如果没有数据，返回 None


# 构建电影类型树
# 在构建树的函数中添加电影的详细信息为节点属性
def build_genre_tree(data):
    if data is None:
        raise ValueError("Input data is None.")

    G = nx.DiGraph()
    root = "Movies by Genre"
    G.add_node(root, level=0)

    # 删除或填充 genre 列中的 NaN 值
    data = data.dropna(subset=['genre'])  # 删除缺失 'genre' 的行

    for genre in data['genre'].unique():
        if genre is not None:  # 确保 genre 不是 None
            G.add_node(genre, level=1)
            G.add_edge(root, genre)
            genre_movies = data[data['genre'] == genre]
            for index, movie in genre_movies.iterrows():
                movie_node = movie['film']
                if pd.notnull(movie_node):  # 确保电影名称不是 None
                    G.add_node(movie_node,
                               level=2,
                               genre=movie['genre'],
                               rotten_tomatoes=movie['rotten_tomatoes'] if pd.notnull(
                                   movie['rotten_tomatoes']) else 'N/A',
                               audience_score=movie['audience_score'] if pd.notnull(movie['audience_score']) else 'N/A',
                               domestic_gross=movie['domestic_gross'] if pd.notnull(movie['domestic_gross']) else 0,
                               foreign_gross=movie['foreign_gross'] if pd.notnull(movie['foreign_gross']) else 0,
                               worldwide_gross=movie['worldwide_gross'] if pd.notnull(movie['worldwide_gross']) else 0,
                               budget=movie['budget'] if pd.notnull(movie['budget']) else 0,
                               oscar=movie['oscar'] if pd.notnull(movie['oscar']) else 'N/A',
                               bafta=movie['bafta'] if pd.notnull(movie['bafta']) else 'N/A')
                    G.add_edge(genre, movie_node)
    return G


# 构建电影公司树
def build_studio_tree(data):
    G = nx.DiGraph()
    root = "Movies by Studio"
    G.add_node(root, level=0)

    # 删除或填充 major_studio 列中的 NaN 值
    # data = data.dropna(subset=['major_studio'])  # 删除缺失 'major_studio' 的行

    for studio in data['major_studio'].unique():
        if studio is not None:  # 确保 studio 不是 None
            G.add_node(studio, level=1)
            G.add_edge(root, studio)
            studio_movies = data[data['major_studio'] == studio]
            for index, movie in studio_movies.iterrows():
                movie_node = movie['film']
                if pd.notnull(movie_node):  # 确保电影名称不是 None
                    G.add_node(movie_node,
                               level=2,
                               genre=movie['genre'],
                               rotten_tomatoes=movie['rotten_tomatoes'] if pd.notnull(
                                   movie['rotten_tomatoes']) else 'N/A',
                               audience_score=movie['audience_score'] if pd.notnull(movie['audience_score']) else 'N/A',
                               domestic_gross=movie['domestic_gross'] if pd.notnull(movie['domestic_gross']) else 0,
                               foreign_gross=movie['foreign_gross'] if pd.notnull(movie['foreign_gross']) else 0,
                               worldwide_gross=movie['worldwide_gross'] if pd.notnull(movie['worldwide_gross']) else 0,
                               budget=movie['budget'] if pd.notnull(movie['budget']) else 0,
                               oscar=movie['oscar'] if pd.notnull(movie['oscar']) else 'N/A',
                               bafta=movie['bafta'] if pd.notnull(movie['bafta']) else 'N/A')
                    G.add_edge(studio, movie_node)
    return G


# 可视化树
def visualize_tree(G, layout='spring'):
    if layout == 'circular':
        pos = nx.circular_layout(G)
    elif layout == 'shell':
        pos = nx.shell_layout(G)
    elif layout == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(G)
    else:
        pos = nx.spring_layout(G)

    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_color = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_color.append(G.nodes[node]['level'])  # 根据节点的层级设置颜色

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=[
            f"{node}<br>Genre: {G.nodes[node].get('genre', 'N/A')}<br>Rating: Rotten Tomatoes {G.nodes[node].get('rotten_tomatoes', 'N/A')}%, Audience {G.nodes[node].get('audience_score', 'N/A')}%"
            f"<br>Domestic Gross: ${float(G.nodes[node].get('domestic_gross', 0)):,.0f}m<br>Foreign Gross: ${float(G.nodes[node].get('foreign_gross', 0)):,.0f}m<br>Worldwide Gross: ${float(G.nodes[node].get('worldwide_gross', 0)):,.0f}m"
            f"<br>Budget: ${float(G.nodes[node].get('budget', 0)):,.0f}m<br>Oscar: {G.nodes[node].get('oscar', 'N/A')}<br>Bafta: {G.nodes[node].get('bafta', 'N/A')}"
            for node in G.nodes()],
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=12,
            color=node_color,
            colorbar=dict(
                thickness=15,
                title='Node Levels',
                xanchor='left',
                titleside='right'
            ),
            line_width=2)
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Tree Visualization',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=40),
                        annotations=[dict(
                            text="Tree Visualization",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False),
                        width=1200,  # 调整宽度
                        height=800  # 调整高度
                    )
                    )
    return fig


# 创建Dash应用
app = Dash(__name__)

# 添加CSS样式
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

app.layout = html.Div([
    html.H1("Hollywood Movies Tree Visualization", style={'textAlign': 'center', 'color': '#7FDBFF'}),
    html.Div([
        html.Div([
            dcc.RangeSlider(
                id='year-range',
                min=2007,
                max=2011,
                step=1,
                marks={i: str(i) for i in range(2007, 2012)},
                value=[2007, 2011]
            )
        ], style={'width': '100%', 'padding': '20px'}),
        html.Div([
            dcc.Dropdown(id='search-dropdown', placeholder='Select a movie or studio...'),
        ], style={'width': '100%', 'padding': '20px'}),
        html.Div([
            dcc.RadioItems(
                id='tree-type',
                options=[
                    {'label': 'Genre Tree', 'value': 'genre'},
                    {'label': 'Studio Tree', 'value': 'studio'}
                ],
                value='genre',
                style={'width': '100%'}
            )
        ], style={'width': '48%', 'display': 'inline-block'})
    ], style={'padding': '10px'}),
    html.Div([
        dcc.RadioItems(
            id='layout-type',
            options=[
                {'label': 'Spring Layout', 'value': 'spring'},
                {'label': 'Circular Layout', 'value': 'circular'},
                {'label': 'Shell Layout', 'value': 'shell'},
                {'label': 'Kamada-Kawai Layout', 'value': 'kamada_kawai'}
            ],
            value='spring',
            style={'width': '100%', 'textAlign': 'center', 'padding': '10px'}
        )
    ], style={'textAlign': 'center'}),
    dcc.Loading(
        id="loading",
        type="circle",
        children=dcc.Graph(id='tree-graph')
    )
], style={'margin': '20px'})


def filter_graph(G, search_value):
    """
    Filter the graph to show only the nodes that match the search value and their direct connections.
    """
    # 将搜索值转化为小写以进行不区分大小写的匹配
    search_value = search_value.lower()
    filtered_graph = nx.DiGraph()
    for node in G.nodes(data=True):
        # 确保节点名称是字符串类型
        node_name = str(node[0]).lower()
        if search_value in node_name:
            # 添加当前节点
            filtered_graph.add_node(node[0], **node[1])
            # 添加与当前节点相连的所有边和节点
            for edge in G.edges(node[0], data=True):
                filtered_graph.add_edge(edge[0], edge[1], **edge[2])
                filtered_graph.add_node(edge[1], **G.nodes[edge[1]])

    return filtered_graph


@app.callback(
    Output('search-dropdown', 'options'),
    [Input('tree-type', 'value'),
     Input('year-range', 'value')]
)
def update_search_options(tree_type, year_range):
    directory = "D:\\My document\\大学\\大三下\\数据可视化\\24Spring-DataVisualization\\Task3-Hollywood\\好莱坞电影数据集\\Hollywood Movie Dataset"
    data = load_data(directory, year_range[0], year_range[1])
    if data is not None:
        if tree_type == 'genre':
            options = [{'label': genre, 'value': genre} for genre in data['genre'].dropna().unique()]
        else:
            options = [{'label': studio, 'value': studio} for studio in data['major_studio'].dropna().unique()]
        return options
    return []



@app.callback(
    Output('tree-graph', 'figure'),
    [Input('year-range', 'value'),
     Input('tree-type', 'value'),
     Input('layout-type', 'value'),
     Input('search-dropdown', 'value')]
)
def update_tree(year_range, tree_type, layout_type, search_value):
    directory = "D:\\My document\\大学\\大三下\\数据可视化\\24Spring-DataVisualization\\Task3-Hollywood\\好莱坞电影数据集\\Hollywood Movie Dataset"
    data = load_data(directory, year_range[0], year_range[1])
    print(data)

    if data is None:
        print("No data available for the selected range.")
        return go.Figure()  # 返回一个空图表

    if tree_type == 'genre':
        tree = build_genre_tree(data)
    else:
        tree = build_studio_tree(data)

    # 如果有搜索值，过滤图以仅显示相关节点
    if search_value:
        tree = filter_graph(tree, search_value)

    return visualize_tree(tree, layout=layout_type)


if __name__ == '__main__':
    app.run_server(debug=True)
