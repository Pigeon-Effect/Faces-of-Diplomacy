# Faces of Diplomacy: Visual Framing of Global Leaders in the *China Daily* (2020–2025)

This repository contains the code and data for analyzing the **emotional portrayal of world leaders** in images published by the state-run newspaper *China Daily* from 2020 to 2025. The analysis combines computer vision, facial recognition, and statistical methods to explore visual media bias in international political communication.

---

## Pipeline Overview

- **Data Collection**: Automated scraping of *China Daily* via Selenium and keyword-based queries.
- **Face Recognition**: Training an SVM classifier using 22,607 Wikimedia images of 225 *de facto* global leaders.
- **Image Processing**: Cropping, normalization, and augmentation of facial images.
- **Emotion Classification**: Applying a ViT-based model to detect 7 facial expressions:  
  *Anger, Disgust, Fear, Happiness, Neutrality, Sadness, Surprise*

---

## Distribution of Leader Depictions  
*Number of recognized appearances by country and continent:*

<img src="https://github.com/Pigeon-Effect/Faces-of-Diplomacy/blob/main/results/treemap.svg?raw=true" style="width:100%; height:auto;">

---

## Emotional Portrayals and Geopolitical Alignment  
*Emotion prevalence by country, sorted by UNGA voting coincidence with China (2020–2025):*

<img src="https://raw.githubusercontent.com/Pigeon-Effect/Faces-of-Diplomacy/refs/heads/main/results/emotion_prevalence_heatmap_all_countries.svg" style="width:100%; height:auto;">

---

## Results Summary

- From **5,202 verified images**, **Xi Jinping alone appears in 1,926** — nearly **37%** of all depictions.
- **Neutrality** and **Happiness** dominate facial expressions across countries.
- **Negative emotions** (*Anger, Fear, Disgust, Surprise*) are more common among leaders from countries **less aligned** with China.
- **Neutrality** is strongly associated with **Chinese allies**, suggesting a diplomatic framing of composure.
- Outlier emotions (e.g., Anger in Cyprus, Surprise in Slovenia) are largely driven by **single-image distortions**.

---

## Correlation with Political Alignment

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

---

## Interpretation

- **Neutrality** is the most reliable indicator of alignment: *China Daily* portrays allied leaders with more emotional restraint.
- **Anger** shows a modest positive correlation with diplomatic opposition to China.
- Contrary to prior assumptions, **Happiness** is not significantly associated with alignment.
- Rather than a simple positive–negative dichotomy, the results point to a **spectrum of emotional expressiveness**, with allies framed as composed and adversaries as emotionally charged.

---
