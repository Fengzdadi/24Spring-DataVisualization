import pandas as pd
import numpy as np
import plotly.graph_objects as go

df = pd.read_excel('data.xlsx', index_col=0)
df[df < 0.73] = np.nan

max_values = df.max(axis=1)
max_columns = df.idxmax(axis=1)

result_df = pd.DataFrame({
    'Position': df.index,
    'Amino Acid': max_columns,
    'Probability': max_values
})

color_map = {
    'low': 'yellow',    # 0.7 <= Probability < 0.8
    'medium': 'orange', # 0.8 <= Probability < 0.9
    'high': 'red',      # Probability >= 0.9
    'NaN': 'grey'       # NaN值
}
def map_probability_to_color(probability):
    if pd.isna(probability):
        return color_map['NaN']
    elif 0.7 <= probability < 0.8:
        return color_map['low']
    elif 0.8 <= probability < 0.9:
        return color_map['medium']
    elif probability >= 0.9:
        return color_map['high']

result_df['Color'] = result_df['Probability'].apply(map_probability_to_color)

fig = go.Figure()

for i, (index, row) in enumerate(result_df.iterrows(), start=1):
    fig.add_trace(go.Bar(
        x=[1],
        y=[row['Position']],
        orientation='h',
        marker=dict(color=row['Color']),
        name=f"{i}. {row['Amino Acid']}" if pd.notna(row['Amino Acid']) else '',
        hoverinfo='text',
        hovertext=f"{row['Amino Acid']}: {row['Probability'] if pd.notna(row['Probability']) else 'N/A'}"
    ))


fig.update_layout(
    title='Most Likely Amino Acid at Each Position with Probability Range',
    xaxis=dict(title='Probability', showticklabels=False),
    yaxis=dict(title='Position'),
    legend_title="Amino Acid",
    height=1000
)

fig.show()
