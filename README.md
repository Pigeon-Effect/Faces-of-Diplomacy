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



Prevalence of Emotions of De Facto-Leaders Depictions by Country (sorted by Voting Coincidence in the UNGA from 2020 to 2025.
<img src="https://raw.githubusercontent.com/Pigeon-Effect/Faces-of-Diplomacy/refs/heads/main/results/emotion_prevalence_heatmap_all_countries.svg" style="width:100%; height:auto;">



Results indicate patterns in emotional representation based on geopolitical alignment.
Neutrality shows the strongest and most robust negative correlation — leaders from countries aligned with China are shown more neutrally
Anger shows a moderate positive correlation, especially among China's rivals
Happiness is not significantly associated with alignment
"Negative emotions" (Anger, Fear, Disgust, Surprise) are more common among leaders from adversarial countries


<table>
  <thead>
    <tr>
      <th>Emotion</th>
      <th>Pearson's <em>r</em> (p-value)</th>
      <th>Kendall's <em>τ</em> (p-value)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Anger</td><td>0.251*** (0.0015)</td><td>0.098* (0.0691)</td></tr>
    <tr><td>Disgust</td><td>0.090 (0.2624)</td><td>0.031 (0.5645)</td></tr>
    <tr><td>Fear</td><td>0.139* (0.0835)</td><td>0.112** (0.0372)</td></tr>
    <tr><td>Happiness</td><td>-0.074 (0.3556)</td><td>-0.095* (0.0775)</td></tr>
    <tr><td>Neutrality</td><td>-0.210** (0.0086)</td><td>-0.158*** (0.0035)</td></tr>
    <tr><td>Sadness</td><td>0.047 (0.5639)</td><td>0.009 (0.8661)</td></tr>
    <tr><td>Surprise</td><td>0.168** (0.0364)</td><td>0.031 (0.5645)</td></tr>
  </tbody>
</table>

<p><strong>Significance levels:</strong><br>
*** p &lt; 0.0071 (Bonferroni adjusted)<br>
** p &lt; 0.05<br>
* p &lt; 0.10</p>

