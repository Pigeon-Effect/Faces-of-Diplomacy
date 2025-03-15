import os
import json
import pandas as pd
import plotly.express as px


def count_images(path):
    """Count image files in a directory and its subdirectories."""
    count = 0
    for root, dirs, files in os.walk(path, followlinks=False):
        count += len([f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'))])
    return count


def analyze_folder_structure(base_path, continent_mapping_path):
    """Analyze the folder structure and count images by continent, country and politician."""
    print("Verifying paths...")
    print(f"Base path exists: {os.path.exists(base_path)}")
    print(f"Mapping exists: {os.path.exists(continent_mapping_path)}")

    print("\nLoading continent mapping...")
    with open(continent_mapping_path, 'r') as f:
        country_to_continent = json.load(f)

    countries = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    total_countries = len(countries)
    print(f"\nProcessing {total_countries} countries:")

    result = []
    continent_counts = {}
    country_counts = {}

    for i, country in enumerate(countries, 1):
        country_path = os.path.join(base_path, country)
        continent = country_to_continent.get(country, "Unknown")
        print(f"\nCountry {i}/{total_countries}: {country} ({continent})")

        politicians = [d for d in os.listdir(country_path) if os.path.isdir(os.path.join(country_path, d))]

        country_total = 0
        for politician in politicians:
            politician_path = os.path.join(country_path, politician)
            image_count = count_images(politician_path)
            if image_count > 0:
                print(f" - {politician}: {image_count} images")
                country_total += image_count
                result.append({
                    'continent': continent,
                    'country': country,
                    'politician': politician,
                    'count': image_count
                })

        if country_total > 0:
            country_counts[country] = country_total
            continent_counts[continent] = continent_counts.get(continent, 0) + country_total

    df = pd.DataFrame(result)
    return df, continent_counts, country_counts


if __name__ == "__main__":
    base_path = r"C:\Users\Admin\Documents\Cultural Analytics\resources\china_daily"
    continent_mapping_path = r"C:\Users\Admin\Documents\Cultural Analytics\resources\country_continent_mapping.json"

    print("\nStarting analysis...")
    df, continent_counts, country_counts = analyze_folder_structure(base_path, continent_mapping_path)

    print("\nCreating visualization...")

    # Calculate total images
    total_images = df['count'].sum()

    # Create labels with counts
    df['continent_label'] = df['continent'].apply(lambda x: f"{x} ({continent_counts.get(x, 0)})")
    df['country_label'] = df['country'].apply(lambda x: f"{x} ({country_counts.get(x, 0)})")

    # Define custom color palette
    custom_colors = ["#e7e7e7", "#01befe", "#ffdd00", "#ff7d00", "#ff006d", "#adff02", "#8f00ff"]

    # Create treemap with total count in world label
    fig = px.treemap(df,
                     path=[px.Constant(f"World ({total_images})"), 'continent_label', 'country_label', 'politician'],
                     values='count',
                     color='continent',
                     color_discrete_sequence=custom_colors)

    # Adjust layout
    fig.update_layout(
        height=900,  # Adjust height to make it upright
        width=700  # Keep width narrower than height
    )

    output_path = os.path.abspath(
        r"C:\Users\Admin\Documents\Cultural Analytics\resources\political_faces_treemap_3000001.html")
    print(f"\nSaving to: {output_path}")
    fig.write_html(output_path)

    print("\nAttempting to display visualization...")
    fig.show()
