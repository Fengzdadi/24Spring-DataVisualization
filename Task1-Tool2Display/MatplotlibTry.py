import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('data.xlsx', index_col=0)
df[df < 0.73] = np.nan  # 忽略概率小于0.73的值

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
    'NaN': 'grey'       # NaN
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


plt.figure(figsize=(3, 10))
for i, (index, row) in enumerate(result_df.iterrows()):
    plt.barh(row['Position'], 1, color=row['Color'], edgecolor='black')
    if pd.notna(row['Amino Acid']):
        plt.text(0.5, i, f"{row['Amino Acid']}", ha='center', va='center', color='black', fontsize=12)


plt.ylabel('Position')
plt.yticks(range(len(result_df)), result_df['Position'])

plt.xlabel('')
plt.xticks([])

import matplotlib.patches as mpatches
legend_handles = [mpatches.Patch(color=color, label=f"{label} Probability") for label, color in color_map.items()]
plt.legend(handles=legend_handles, loc='best')

plt.title('Most Likely Amino Acid at Each Position with Probability Range')
plt.tight_layout()
plt.show()
