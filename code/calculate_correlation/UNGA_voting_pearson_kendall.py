import pandas as pd
from scipy.stats import pearsonr, kendalltau

# Read data
emotion_df = pd.read_csv(r'C:\Users\Admin\Documents\Cultural Analytics\code\facial_expression_recognition\country_emotion_results_only_20_and_more.csv')
order_df = pd.read_csv(r'C:\Users\Admin\Documents\Cultural Analytics\code\facial_expression_recognition\country_order.csv', header=None, names=['iso'])

# Add ranking to order data
order_df['rank'] = range(1, len(order_df)+1)

# Merge with emotion data
merged_df = pd.merge(emotion_df, order_df, on='iso', how='inner')

# Select emotion columns
emotion_columns = ['anger_avg', 'disgust_avg', 'fear_avg', 'happy_avg',
                  'neutral_avg', 'sad_avg', 'surprise_avg']

# Calculate correlations
results = []
for col in emotion_columns:
    pearson_corr, _ = pearsonr(merged_df['rank'], merged_df[col])
    kendall_corr, _ = kendalltau(merged_df['rank'], merged_df[col])
    results.append({
        'Emotion': col,
        'Pearson_r': round(pearson_corr, 3),
        'Kendall_tau': round(kendall_corr, 3)
    })

# Convert to DataFrame for display
results_df = pd.DataFrame(results)
print(results_df)