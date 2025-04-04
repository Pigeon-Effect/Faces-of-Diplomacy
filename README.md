Faces of Diplomacy: Visual Framing of Global Leaders in the China Daily (2020–2025)

This repository contains the code and data for analyzing the emotional portrayal of world leaders in China Daily images from 2020 to 2025. The pipeline includes:

Data Collection: Automated scraping of China Daily images via Selenium and query-based searches.
Face Recognition: Training an SVM classifier on Wikimedia images to identify 225 de facto leaders.
Image Processing: Face cropping, normalization, and augmentation.
Sentiment Analysis: Applying ViT-based facial expression recognition to classify emotions (anger, disgust, fear, happiness, neutrality, sadness, surprise).
Statistical Analysis: Correlation between leader sentiment and UN voting alignment with China.

Results:

Distribution of Recognized De-Facto Leaders by Country and Continent
<img src="https://github.com/Pigeon-Effect/Faces-of-Diplomacy/blob/main/results/treemap.svg?raw=true" style="width:100%; height:auto;">



Prevalence of Emotions of De Facto-Leaders Depictions by Country
<img src="https://raw.githubusercontent.com/Pigeon-Effect/Faces-of-Diplomacy/refs/heads/main/results/emotion_prevalence_heatmap_all_countries.svg" style="width:100%; height:auto;">



Results indicate patterns in emotional representation based on geopolitical alignment.
