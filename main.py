import requests
import pandas as pd
import streamlit as st 
from pyproj import Transformer

#auth_url = "https://services.geodataonline.no/arcgis/tokens/"
token = "UiG8WJ3_CDb2GAiRQ1AY9N3CEuwQwulzzmogbEnJpIg."

# Define layer URL
layer_url = "https://services.geodataonline.no/arcgis/rest/services/Geomap_UTM33_EUREF89/GeomapBedrifter/MapServer/0/query"

# Convert lat/lon to UTM33 (EPSG:25833)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:25833", always_xy=True)
xmin, ymin = transformer.transform(5.3015441, 60.3840685)
xmax, ymax = transformer.transform(5.3026, 60.3913)

# Parameters
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

# Send request
response = requests.get(layer_url, params=params)
data = response.json()

st.write(data)

# Extract features
features = data.get("features")

# Convert to DataFrame
if features:
    df = pd.DataFrame([f["attributes"] for f in features])
    df.to_csv("arcgis_features.csv", index=False, encoding="utf-8")
    print("CSV saved successfully!")
else:
    print("No data found.")

