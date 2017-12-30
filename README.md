# RealTerrain

RealTerrain is a small Python3 script which aims to make it easier to convert
USGS elevation data (IMG, ArcGrid or GeoTIFF format supported) into high quality 
16-bit PNG files suitable for use as heightmaps in modern game engines.

This script uses the compiled GDAL binaries for Windows provided by 
[GIS Internals](http://www.gisinternals.com/release.php) so you will need to run
this script on a Windows machine.

## Installation Instructions
Simply download or clone this repository, no additional installation is required.

## How to download USGS Elevation Data
There are several ways to download high-quality, free elevation data from the 
United States Geological Survey (USGS) website.

The easiest is to use the interactive map at 
[https://viewer.nationalmap.gov/basic/](https://viewer.nationalmap.gov/basic/).

Expand the __Elevation Products (3DEP)__ section which will allow you to select
which dataset you would like to get elevation data for. The data sets that you 
will be interested in are as follows, with the '1 meter DEM' being the highest 
quality:
* 1 meter DEM
* 1/9 arc-second DEM (~3m resolution)
* 1/3 arc-second DEM (~10m resolution)
* 1 arc-second DEM (~30m resolution)
* 2 arc-second DEM - Alaska (~60m resolution)
* 5 meter DEM - Alaska

Note that, although 1 meter DEM provides the highest resolution data, the
coverage is a lot less than the other data sets. You can toggle the coverage of
each data set by clicking the 'Show Availability' link under each tickbox.

More information about the data sets can be found 
[here](https://nationalmap.gov/3DEP/3dep_prodserv.html).

For this guide, I will select '1 meter DEM', click 'Show Availability' and 
zoom to an area of the map that has coverage.

With a suitable area centered in the view, click the 'Find Products' button and
you will get a list of all the elevation data which exists within the area you
selected. Scroll through the list and look for interesting topology from the
thumbnail view. Click the 'Download' link to download one of the files.

__Important__: The file formats compatabile with this script are IMG, ArcGrid
and GeoTIFF.

## RealTerrain Usage Instructions

I'm assuming that you have now downloaded a dataset from the USGS website, in
either IMG or ArgGrid format. If not, please read the previous section.

### IMG Instructions

1. Extract the ZIP file
2. Move the .img file into the input/ folder within the real-terrain directory

### ArcGrid Instructions

1. Extract the ZIP file
2. Within one of the extracted directories there will be a large ADF file.
Move this entire directory into the input/ folder within the real-terrain directory

### Usage
```
python real-terrain.py --help
usage: real-terrain.py [-h] [-r output_resolution] input_data

Generate a 16-bit PNG heightmap from USGS data

positional arguments:
  input_data            Name of the input data (IMG, ArcGrid or GeoTIFF)

optional arguments:
  -h, --help            show this help message and exit
  -r output_resolution  Resolution of the final output (default 4096x4096)
```

If you are converting from an IMG or GeoTIFF file, simply specify the name of the 
file within the /input folder that you want to convert. For example:
```python
python real-terrain.py my_img_input.img
```

Otherwise, if you are converting from ArcGrid, you need to specify the ArcGrid
directory. For example:
```python
python real-terrain.py my_arcgrid_input
```

You can optionally change the default resolution which the heightmap will output to:
```python
python real-terrain.py my_img_input.img -r 8192
```
The default resolution is 4096 x 4096.

The script will also output the minimum and maximum elevation values (in meters)
for the terrain which you should take a note of for use within your Game Engine.

All converted heightmaps can be found in the output/ directory in the format
`20170812_181455_heightmap.png`. You can delete everything from input/ and output/
when you are finished.