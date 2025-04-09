import requests
import pandas as pd
from pyproj import Transformer
from time import sleep
import os

# API token and layer URL
token = "UiG8WJ3_CDb2GAiRQ1AY9N3CEuwQwulzzmogbEnJpIg."
layer_url = f"https://services.geodataonline.no/arcgis/rest/services/Geomap_UTM33_EUREF89/GeomapMatrikkelEier/MapServer/1/query"

# Coordinate transformer: WGS84 -> UTM33
transformer = Transformer.from_crs("EPSG:4326", "EPSG:25833", always_xy=True)

# Define bounding box over Norway (approx)
lon_min, lon_max = 4.5, 31.0
lat_min, lat_max = 57.8, 71.2

# Grid step size (degrees)
step_lon = 0.05
step_lat = 0.05

# Output CSV
output_file = "GeomapMatrikkelEier.csv"
first_write = True  # To write header only once

# Remove old file if it exists
if os.path.exists(output_file):
    os.remove(output_file)

# Loop through grid
lon = lon_min
while lon < lon_max:
    lat = lat_min
    while lat < lat_max:
        xmin_deg, ymin_deg = lon, lat
        xmax_deg, ymax_deg = lon + step_lon, lat + step_lat

        # Convert to UTM33
        xmin, ymin = transformer.transform(xmin_deg, ymin_deg)
        xmax, ymax = transformer.transform(xmax_deg, ymax_deg)

        params = {
            "where": "1=1",
            "geometry": f"{xmin},{ymin},{xmax},{ymax}",
            "geometryType": "esriGeometryEnvelope",
            "spatialRel": "esriSpatialRelIntersects",
            "outFields": "*",
            "f": "json",
            "outSR": "25833",
            "token": token
        }

        try:
            response = requests.get(layer_url, params=params)
            data = response.json()

            features = data.get("features", [])
            if features:
                df = pd.DataFrame([{**f["attributes"], **{"geometry": f.get("geometry")}} for f in features])

                # Append to CSV
                df.to_csv(output_file, mode='a', index=False, encoding="utf-8", header=first_write)
                first_write = False  # After first write, skip header

                print(f"Wrote {len(df)} rows from ({lon:.2f}, {lat:.2f})")

        except Exception as e:
            print(f"Error at ({lon:.2f}, {lat:.2f}): {e}")

        sleep(0.2)
        lat += step_lat
    lon += step_lon

print("Finished downloading and writing all data.")
