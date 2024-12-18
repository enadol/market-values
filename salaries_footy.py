"""Import necessary packages."""
import json
import matplotlib.pyplot as plt
import pandas as pd


# Read JSON file 'salaries_footystats.json'
with open('salaries_footystats.json', 'r', encoding='utf-8') as f:
    # Load file as JSON
    data = json.load(f)

# Convert JSON to DataFrame
df = pd.DataFrame(data['players'])

# Take the % character out of values in the Change column and convert to numeric
df['Change'] = df['Change'].str.rstrip('%').astype('float')

# Create a clean DataFrame by excluding NaN values in the Change column
df_clean = df.dropna(subset=['Change'])

# Limit the clean DataFrame to the top 20 rows
df_clean = df_clean.head(50).reset_index(drop=True)

# Create a new column 'color' based on the values of 'Change'
df_clean['color'] = ['green' if x > 0 else 'red' for x in df_clean['Change']]

# create a chart with matplotlib
fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(df_clean['Player'], df_clean['Change'], color=df_clean['color'])
ax.set_xlabel('Market Value Change (in %)')
ax.set_ylabel('Player Name')
ax.set_title('Bundesliga Players Market Value Change 2024 vs 2023')
ax.invert_yaxis()  # labels read top-to-bottom
# add value labels to the bars sligthly outside each bar
for i, v in enumerate(df_clean['Change']):
    # if value is positive, place label to the right of the bar, else to the left
    if v > 0:
        ax.text(v + 0.5, i, str(v) + '%', color='black', va='center', fontweight='bold')
    else:
        ax.text(v - 0.5, i, str(v) + '%', color='black', va='center', fontweight='bold', ha='right')
# add the player name in the bar font in white
for i, bar in enumerate(bars):
    ax.text(bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, df_clean['Player'][i],\
        ha='center', va='center', fontsize=6, color='white', fontweight='bold')
# don't show players name in the y-axis
ax.set_yticklabels([])
# remove the spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
# remove the ticks
ax.tick_params(axis='both', which='both', bottom=False, top=False, labelbottom=True,\
    left=False, right=False, labelleft=False)
# add a grid
ax.grid(axis='x', linestyle='--', alpha=0.7)
# add a background color to the chart
ax.set_facecolor('#f5f5f5')
# add annotacion for source 'Source: Transfermarkt.de & FootsyStats.com' in the bottom right corner
ax.annotate('Source: Transfermarkt.de & FootsyStats.com', xy=(1, 0), xycoords='axes fraction',\
    fontsize=6, xytext=(-5, 5), textcoords='offset points', ha='right', va='bottom',\
    bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.5))
# add annotacion for chart author '@EnriqueALopezM' in the bottom left corner
ax.annotate('Chart: @EnriqueALopezM', xy=(0, 0), xycoords='axes fraction',\
    fontsize=12, xytext=(5, 5), textcoords='offset points', ha='left', va='bottom',\
    bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.5))

# show the chart
plt.show()
# save the chart as a png file
fig.savefig('bundesliga_players_market_value_change_2024_vs_2023.png', dpi=300, bbox_inches='tight')
