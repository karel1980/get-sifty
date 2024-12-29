from PIL import Image
import requests
from io import BytesIO
import sys
import json

import math


def lat_lon_to_tile(lat, lon, zoom):
    n = 2 ** zoom
    x = int(n * ((lon + 180) / 360))
    y = int(n * (1 - (math.log(math.tan(math.radians(lat)) + (1 / math.cos(math.radians(lat)))) / math.pi)) / 2)
    return x, y

def get_tile_url(x, y, zoom):
    url = f"http://localhost:8080/styles/dark/512/{zoom}/{x}/{y}.png"
    print(f"downloading {url}")
    return url

def fetch_tile(x, y, zoom):
    tile_url = get_tile_url(x, y, zoom)
    response = requests.get(tile_url)
    return Image.open(BytesIO(response.content))

def create_static_maps(center_lat, center_lon, zoom, base_name):
    print(f"Generating static maps for {base_name}")
    x_center,y_center = lat_lon_to_tile(center_lat, center_lon, zoom)

    for x in range(x_center - 10, x_center + 7, 4):
        for y in range(y_center - 10, y_center + 7, 4):
            create_static_map(x, x+5, y, y+5, zoom, base_name) 

def create_static_map(x0, x1, y0, y1, zoom, base_name):
    tile_images = []
    grid_size = x1-x0
    for y in range(y0, y1):
        for x in range(x0, x1):
            tile_images.append(fetch_tile(x, y, zoom))

    # Combine tiles into a single image
    width, height = tile_images[0].size
    combined_image = Image.new('RGB', (width * grid_size, height * grid_size))

    for i, tile in enumerate(tile_images):
        x = (i % grid_size) * width
        y = (i // grid_size) * height
        combined_image.paste(tile, (x, y))

    filename = f"static-maps/{base_name}_{x0}_{y0}-static.png"
    print(f"saving {filename}")
    combined_image.save(f"static-maps/{base_name}_{x0}_{y0}-static.png")


def main():
    # Example usage
    name = sys.argv[1]

    countries = json.load(open('restcountries.json'))
    lookup = {}
    for c in countries:
        if "capital" in c and "capitalInfo" in c and "latlng" in c["capitalInfo"]:
            key = c["capital"][0].lower().replace(" ","-")
            lookup[key] = c["capitalInfo"]["latlng"]
    
    if name not in lookup:
        print(f"Location {name} not found")
        sys.exit(1)

    lat,lon = lookup[name]
    create_static_maps(lat, lon, 15, name)

if __name__ =="__main__":
    main()
