import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.io as pio


# 读取数据
def load_data(directory, start_year, end_year):
    all_data = []
    for year in range(start_year, end_year + 1):
        file_path = os.path.join(directory, f"Most Profitable Hollywood Stories - US {year}.csv")
        if os.path.exists(file_path):
            yearly_data = pd.read_csv(file_path)
            yearly_data['Year'] = year
            all_data.append(yearly_data)
    return pd.concat(all_data, ignore_index=True)


# 构建电影类型树
def build_genre_tree(data):
    G = nx.DiGraph()
    root = "Movies by Genre"
    G.add_node(root)
    for genre in data['Genre'].unique():
        G.add_node(genre)
        G.add_edge(root, genre)
        genre_movies = data[data['Genre'] == genre]
        for movie in genre_movies['Film']:
            G.add_node(movie)
            G.add_edge(genre, movie)
    return G


# 构建电影公司树
def build_studio_tree(data):
    G = nx.DiGraph()
    root = "Movies by Studio"
    G.add_node(root)
    for studio in data['Major Studio'].unique():
        G.add_node(studio)
        G.add_edge(root, studio)
        studio_movies = data[data['Major Studio'] == studio]
        for movie in studio_movies['Film']:
            G.add_node(movie)
            G.add_edge(studio, movie)
    return G


# 可视化树
def visualize_tree(G):
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
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[str(node) for node in G.nodes()],
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        annotations=[dict(
                            text="Tree Visualization",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False))
                    )
    return fig


# 创建Dash应用
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Hollywood Movies Tree Visualization"),
    dcc.Dropdown(
        id='year-range',
        options=[{'label': f'{year}', 'value': year} for year in range(2007, 2012)],
        multi=True,
        value=[2007]
    ),
    dcc.RadioItems(
        id='tree-type',
        options=[
            {'label': 'Genre Tree', 'value': 'genre'},
            {'label': 'Studio Tree', 'value': 'studio'}
        ],
        value='genre'
    ),
    dcc.Graph(id='tree-graph')
])


@app.callback(
    Output('tree-graph', 'figure'),
    Input('year-range', 'value'),
    Input('tree-type', 'value'))
def update_tree(year_range, tree_type):
    directory = "path/to/your/dataset"  # 替换为数据集目录路径
    data = load_data(directory, min(year_range), max(year_range))
    if tree_type == 'genre':
        tree = build_genre_tree(data)
    else:
        tree = build_studio_tree(data)
    return visualize_tree(tree)


if __name__ == '__main__':
    app.run_server(debug=True)
