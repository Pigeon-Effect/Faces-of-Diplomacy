import pandas as pd
from scipy.stats import pearsonr, kendalltau

# Read data
emotion_df = pd.read_csv("country_emotion_results_only_20_and_more.csv")
order_df = pd.read_csv("heatmap_country_order", header=None, names=['iso'])

# Add ranking (1 = highest rank)
order_df['rank'] = range(1, len(order_df) + 1)

# Merge datasets
merged_df = pd.merge(emotion_df, order_df, on='iso', how='inner')

# Select emotion columns
emotion_columns = ['anger_avg', 'disgust_avg', 'fear_avg',
                   'happy_avg', 'neutral_avg', 'sad_avg', 'surprise_avg']

results = []

for col in emotion_columns:
    # Pearson correlation
    pearson_r, pearson_p = pearsonr(merged_df['rank'], merged_df[col])

    # Kendall's tau
    kendall_tau, kendall_p = kendalltau(merged_df['rank'], merged_df[col])

    results.append({
        'Emotion': col,
        'Pearson_r': round(pearson_r, 3),
        'Pearson_p': round(pearson_p, 4),
        'Kendall_tau': round(kendall_tau, 3),
        'Kendall_p': round(kendall_p, 4)
    })

# Convert to DataFrame
results_df = pd.DataFrame(results)
print(results_df)
