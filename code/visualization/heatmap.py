import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("country_emotion_results.csv")

# Load country order from CSV
country_order = pd.read_csv(
    r"C:\Users\Admin\Documents\Cultural Analytics\code\facial_expression_recognition\country_order.csv", header=None)
country_order = country_order[0].tolist()

# Reorder DataFrame
df['iso'] = pd.Categorical(df['iso'], categories=country_order, ordered=True)
df = df.sort_values('iso')

# Prepare data with renamed columns
heatmap_data = df.set_index('iso')[['angry_avg', 'disgust_avg', 'fear_avg',
                                    'happy_avg', 'neutral_avg', 'sad_avg',
                                    'surprise_avg']]
heatmap_data.columns = ['Anger', 'Disgust', 'Fear', 'Happiness',
                        'Neutrality', 'Sadness', 'Surprise']  # New column names

# ... rest of the original code remains EXACTLY the same ...

# Calculate figure dimensions for 1:1.3 aspect ratio within A4
a4_width = 8.27
desired_aspect_ratio = 1 / 1.3
max_fig_height = a4_width / desired_aspect_ratio
fig_height = min(max_fig_height, 11.69)
fig_width = fig_height * desired_aspect_ratio

# Create figure and axes
plt.figure(figsize=(fig_width, fig_height))
ax = sns.heatmap(
    heatmap_data,
    annot=False,
    cmap="YlGnBu",
    linewidths=0.5,          # Border width between cells
    linecolor='black',       # Border color
    cbar=True,
    cbar_kws={
        'orientation': 'vertical',
        'pad': 0.03,
        'aspect': 40,
        'shrink': 1.0,
        'ticks': [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        'format': '%.1f'
    }
)

# Add black border around the entire heatmap
for _, spine in ax.spines.items():
    spine.set_visible(True)
    spine.set_edgecolor('black')
    spine.set_linewidth(0.5)  # Match cell border width

# Colorbar border (same width)
cbar_ax = ax.collections[0].colorbar.ax
for spine in cbar_ax.spines.values():
    spine.set_edgecolor('black')
    spine.set_linewidth(0.5)  # Match cell border width

# Remove y-axis labels
ax.set_yticklabels([])
ax.set_ylabel('')
ax.tick_params(axis='y', length=0, left=False)

# Add country annotations
EVEN_OFFSET = -10
ODD_OFFSET = -50
FONT_SIZE = 7
y_centers = [i + 0.5 for i in range(len(heatmap_data))]

for idx, (y_pos, iso_code) in enumerate(zip(y_centers, heatmap_data.index)):
    offset = EVEN_OFFSET if idx % 2 == 0 else ODD_OFFSET
    ha_align = 'right' if idx % 2 == 0 else 'left'

    ax.annotate(
        iso_code,
        xy=(0, y_pos),
        xytext=(offset, 0),
        textcoords='offset points',
        ha=ha_align,
        va='center',
        fontsize=FONT_SIZE,
        arrowprops=dict(arrowstyle="-", color='black', lw=0.5)
    )

# Final adjustments
ax.tick_params(axis='x', which='both', bottom=False, top=True, labeltop=True, labelbottom=False)  # Move labels to top
plt.xticks(rotation=45, fontsize=10, ha='left')  # Change alignment to left after rotation
plt.subplots_adjust(left=0.25, right=0.93, top=0.95, bottom=0.1)  # Increased right margin space
plt.tight_layout()

# Save and show
output_file = "emotion_prevalence_heatmap_final_v2.svg"
plt.savefig(output_file, format="svg", dpi=300, bbox_inches="tight")
print(f"Heatmap saved as {output_file}")
plt.show()