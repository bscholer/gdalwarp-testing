import subprocess

import numpy as np
from osgeo import gdal
import pyproj

# Paths and SRS details
input_tiff = "/data/bardstown_itrf_no_crs.tif"
source_srs = "EPSG:7912"
target_srs = "EPSG:7912"
source_epoch = 2024
target_epoch = 2010
# transformer = coordinates.TransformerFactory(source_srs, target_srs, target_epoch, 'NOAM').build()
# custom_proj_pipeline = transformer.definition
custom_proj_pipeline = "proj=pipeline ellps=GRS80 step proj=unitconvert xy_in=deg xy_out=rad step proj=cart step inv init=ITRF2014:NOAM t_epoch=2010.0 step inv proj=cart step proj=unitconvert xy_in=rad xy_out=deg"

# Define the string to insert
insert_string = f" step proj=set v_4={source_epoch}"

# Find the index to insert the string
insert_index = custom_proj_pipeline.find("ellps=GRS80") + len("ellps=GRS80")

# Insert the string
custom_proj_pipeline = custom_proj_pipeline[:insert_index] + insert_string + custom_proj_pipeline[insert_index:]

print("proj pipeline:\t", custom_proj_pipeline)

# List of test configurations
test_cases = [
    {"name": "-s_srs, -t_srs", "params": ["-s_srs", source_srs, "-t_srs", target_srs]},
    {
        "name": "-s_srs, -t_srs, -s_coord_epoch",
        "params": ["-s_srs", source_srs, "-s_coord_epoch", str(source_epoch), "-t_srs", target_srs],
    },
    {
        "name": "-s_srs, -t_srs, -s_coord_epoch, -t_coord_epoch",
        "params": [
            "-s_srs",
            source_srs,
            "-s_coord_epoch",
            str(source_epoch),
            "-t_srs",
            target_srs,
            "-t_coord_epoch",
            str(target_epoch),
        ],
    },
    {"name": "-ct", "params": ["-ct", custom_proj_pipeline]},
    {"name": "-t_srs, -ct", "params": ["-ct", custom_proj_pipeline, "-t_srs", target_srs]},
    {"name": "-s_srs, -ct", "params": ["-ct", custom_proj_pipeline, "-s_srs", source_srs]},
    {
        "name": "-s_srs, -t_srs, -s_coord_epoch, -t_coord_epoch, -ct",
        "params": [
            "-s_srs",
            source_srs,
            "-s_coord_epoch",
            str(source_epoch),
            "-t_srs",
            target_srs,
            "-t_coord_epoch",
            str(target_epoch),
            "-ct",
            custom_proj_pipeline,
        ],
    },
]

for i, test in enumerate(test_cases):
    test["name"] = f"{i}_{test['name']}"
    test["name"] = test["name"].replace("/", "_")

WGS84_GEODESIC = pyproj.geod.Geod(ellps='WGS84')

def geodesic_distance(longitude1: float, latitude1: float, longitude2: float, latitude2: float) -> float:
    """Compute the geodesic distance between pair(s) of points, using GeographicLib (via PyProj)."""
    _, _, distance_meters = WGS84_GEODESIC.inv(longitude1, latitude1, longitude2, latitude2)
    return distance_meters


# Function to get the boundaries of a TIFF file
def get_tiff_boundaries(tiff_path):
    ds = gdal.Open(tiff_path)
    if not ds:
        print(f"Failed to open {tiff_path}")
        return None
    gt = ds.GetGeoTransform()
    minx = gt[0]
    miny = gt[3] + gt[5] * ds.RasterYSize
    maxx = gt[0] + gt[1] * ds.RasterXSize
    maxy = gt[3]
    # print(minx)
    return (minx, miny, maxx, maxy)


x, y = get_tiff_boundaries(input_tiff)[:2]
# print(x, y)
# print("original tiff boundaries:", get_tiff_boundaries(input_tiff))
# correct_top_left_itrf = (itrf_coords[0], itrf_coords[1], 0, 0)[0:2]
# print("correct top left itrf:", correct_top_left_itrf)
# print("============")

print("====================================")
print("original top left itrf:", x, y)
correct_top_left_itrf = (-85.41192286502883, 37.81018471550539)
print("correct top left itrf:", correct_top_left_itrf)
print("distance from 2024 to 2010, via pyproj transformer:", geodesic_distance(correct_top_left_itrf[0], correct_top_left_itrf[1], x, y))
print("====================================")

# Run tests and store boundaries
test_boundaries = {}
distances_from_correct = {}
for test in test_cases:
    output_tiff = f"{test['name']}_reprojected.tif"
    gdalwarp_command = ["gdalwarp"] + test["params"] + [input_tiff, output_tiff]

    # Run the gdalwarp command
    result = subprocess.run(gdalwarp_command, capture_output=True, text=True)

    # Check for errors
    if result.returncode != 0:
        print(f"Error running {test['name']}:")
        print(result.stderr)
    else:
        # print(f"{test['name']} ran successfully:")
        # print(result.stdout)
        # Get and store the boundaries
        boundaries = get_tiff_boundaries(output_tiff)
        print(f"{test['name']} boundaries:", boundaries)
        if boundaries:
            test_boundaries[test['name']] = boundaries
            # print(f"{test['name']} boundaries: {boundaries}")
            distances_from_correct[test['name']] = geodesic_distance(
                correct_top_left_itrf[0], correct_top_left_itrf[1], boundaries[0], boundaries[1]
            )
            print(
                "distance from correct:",
                geodesic_distance(correct_top_left_itrf[0], correct_top_left_itrf[1], boundaries[0], boundaries[1]),
            )
            if np.isclose(
                geodesic_distance(correct_top_left_itrf[0], correct_top_left_itrf[1], boundaries[0], boundaries[1]),
                0,
                atol=0.01,
            ):
                print(" 🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉 correct top left itrf")

max_test_name_len = max(len(test["name"]) for test in test_cases)

print("\ngdalwarp parameters | Distance")
print("-----")
for test, distance in distances_from_correct.items():
    print(f"{test[2:].ljust(max_test_name_len + 1)} | {distance}")
