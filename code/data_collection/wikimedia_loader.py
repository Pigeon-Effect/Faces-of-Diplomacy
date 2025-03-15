import requests
import os
import pandas as pd

def extract_wikimedia_image_links(query, base_folder, limit=200):
    # Create the base folder if it doesn't exist
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    # Create the query-specific folder within the base folder
    query_folder = os.path.join(base_folder, query.replace(" ", "_"))
    if not os.path.exists(query_folder):
        os.makedirs(query_folder)

    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": f"file:{query}",
        "srlimit": limit,
        "srprop": "snippet",
        "srwhat": "text",
        "srsort": "relevance"
    }
    response = requests.get(url, params=params).json()
    search_results = response.get("query", {}).get("search", [])

    # Create a DataFrame to store the image links
    image_links = []
    for result in search_results:
        title = result.get("title")
        if title and title.startswith("File:"):
            # Extract the file name from the title
            file_name = title.split("File:")[-1].strip()
            # Check if the file is a JPG or PNG
            if file_name.lower().endswith(('.jpg', '.png')):
                # Construct the direct image URL
                image_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{file_name}"
                image_links.append(image_url)
                print(f"Extracted link: {image_url}")

    # Save the image links to a DataFrame
    df = pd.DataFrame(image_links, columns=["image_url"])
    return df, query_folder

def download_images_from_links(df, query_folder, query, limit=200):
    headers = {
        "User-Agent": "My Wikimedia Downloader Script/1.0 (your-email@example.com)"
    }

    # Initialize a counter for naming the images
    image_counter = 1

    for index, row in df.iterrows():
        if image_counter > limit:
            break
        link = row["image_url"]
        try:
            response = requests.get(link, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes

            # Create a standardized filename
            sanitized_query = query.replace(" ", "_")
            filename = f"{sanitized_query}_{image_counter:03d}.jpg"  # Use 3-digit padding

            # Define the save path within the query folder
            save_path = os.path.join(query_folder, filename)

            with open(save_path, "wb") as f:
                f.write(response.content)

            print(f"Downloaded {filename} to {save_path}")
            image_counter += 1
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {link}: {e}")

# Read the CSV file
csv_file = "wikimedia_dataset/De_Facto_Leader.csv"
df_leaders = pd.read_csv(csv_file, sep=";")

# Iterate through each row in the CSV
for index, row in df_leaders.iterrows():
    country_code = row["Country_Code"]
    leaders = row["De_Facto_Leader"].split(", ")

    for leader in leaders:
        print(f"Processing {leader} for {country_code}")
        base_folder = os.path.join("wikimedia_dataset", country_code)
        df_images, leader_folder = extract_wikimedia_image_links(leader, base_folder, limit=200)
        download_images_from_links(df_images, leader_folder, leader, limit=200)