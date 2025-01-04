import requests

# TMDb API Details
API_KEY = "bf4119a66b1bf5c2fdb1140d5a36cbfe"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# GitHub File Details
RAW_URL = "https://raw.githubusercontent.com/markgithub29/My-playlist/refs/heads/main/devara.m3u"
UPDATED_FILE_PATH = "updated_playlist.m3u"

# Fetch the M3U file from GitHub
response = requests.get(RAW_URL)
m3u_content = response.text.splitlines()

updated_content = ["#EXTM3U"]

for line in m3u_content:
    if line.startswith("#EXTINF"):
        # Extract movie name
        movie_name = line.split(",", 1)[-1].strip()

        # Fetch movie details from TMDb
        tmdb_response = requests.get(f"{TMDB_BASE_URL}/search/movie", params={"api_key": API_KEY, "query": movie_name})
        tmdb_data = tmdb_response.json()

        if tmdb_data["results"]:
            # Get the poster path
            poster_path = tmdb_data["results"][0]["poster_path"]
            poster_url = f"{IMAGE_BASE_URL}{poster_path}"
            updated_content.append(f'#EXTINF:-1 tvg-logo="{poster_url}",{movie_name}')
        else:
            updated_content.append(line)  # If no match found, keep original line
    else:
        updated_content.append(line)  # Keep stream links unchanged

# Save updated M3U file
with open(UPDATED_FILE_PATH, "w") as file:
    file.write("\n".join(updated_content))

print(f"Updated M3U file saved as {UPDATED_FILE_PATH}")
