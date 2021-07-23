# SWAV Surface Water Area Variations

SWAV is a collection of Python scripts used to estimate water surface area variations of lakes and reservoirs globally from Synthetic Aperature Radar (SAR) observations from the European Space Agency's Sentinel-1 Mission. The scripts utilize Google Earth Engine (GEE) for data access and processing. Also included are scripts to provide global and continental scale analysis of the derived surface area variations.

## Google Earth Engine Python API Installation
This software makes use of the GEE Python API, which can be installed by following instructions [here]https://developers.google.com/earth-engine/guides/python_install. Additionally, users need to register for a GEE account, which can be found [here]https://signup.earthengine.google.com.

## Acquisition of HydroLakes Database
All data used by this software is hosted by GEE, except for the HydroLakes Database, which need to be uploaded to individual user GEE accounts as private assets. To download the database, click [here]https://hydrosheds.org/page/hydrolakes and download the "Lake polygons (including all attributes) in a Shapefile" file. Unzip the file, and upload the file to GEE as an asset through GEE's [web API]https://code.earthengine.google.com/.
