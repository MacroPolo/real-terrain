# RealTerrain

RealTerrain is a small Python3 script which aims to make it easier to convert
USGS elevation data (IMG, ArcGrid or GeoTIFF format supported) into high quality 
16-bit PNG files suitable for use as heightmaps in modern game engines.

This script uses the compiled GDAL binaries for Windows provided by 
[GIS Internals](http://www.gisinternals.com/release.php) so you will need to run
this script on a Windows machine.

## Installation Instructions

* Download or clone this repository.
* Install the [Pillow](https://pillow.readthedocs.io/en/3.0.x/installation.html#basic-installation)
library to allow image manipulation. Easily achieved with `pip`:

```python
pip install Pillow
```

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

1. Extract the ZIP file.
2. Move the .img file into the `input/` folder within the real-terrain directory.

### ArcGrid Instructions

1. Extract the ZIP file.
2. Within one of the extracted directories there will be a large ADF file.
Move this entire directory into the `input/` folder within the real-terrain directory.

### Usage

```
$ python real-terrain.py --help
usage: real-terrain.py [-h] [-s scale] [-t tile] [-r random] dem

Generate 16-bit PNG heightmaps from geospatial DEM files (IMG, GeoTiff and
ArcGrid).

positional arguments:
  dem         File (IMG, GeoTiff) or folder (ArcGrid) name of the source data
              located in 'input\' which you would like to convert.

optional arguments:
  -h, --help  show this help message and exit
  -s scale    Scale the full resolution heighmap to a fixed resolution.
  -t tile     Slice the full resolution heighmap into sequential tiles.
  -r random   Slice the full resolution heighmap into random tiles.
```

If you are converting from an IMG or GeoTIFF file, simply specify the name of the 
file within the `/input` folder that you want to convert. For example:

```python
python real-terrain.py my_img_input.img
```

Otherwise, if you are converting from ArcGrid, you need to specify the ArcGrid
directory. For example:

```python
python real-terrain.py my_arcgrid_input
```

By default, the script will output a full-resolution 16-Bit PNG convereted from your
input data.

The `scale` option will output an additional heightmap which has been scaled to your 
resolution of choice (square resolution).

The `tile` option will also slice the original heighmap into sequential tiles of whatever 
resolution you set.

The `random` option performs the same action as `tile` however the slices are random, rather 
than sequential.

Example with all options enabled:

```python
$ python real-terrain.py -s 2048 -t 512 -r 4096 input.img
>>> Extracting elevation information from input DEM.
Minimum elevation: 650m
Maximum elevation: 2455m
Elevation range: 1805m

>>> Converting input DEM to full resolution 16-bit PNG.
Input file size is 10812, 10812
0...10...20...30...40...50...60...70...80...90...100 - done.

>>> Converting input data to scaled resolution 16-bit PNG
Input file size is 10812, 10812
0...10...20...30...40...50...60...70...80...90...100 - done.

>>> Slicing full resolution heightmap into sequential tiles.

>>> Slicing full resolution heightmap into random tiles.
(1) Bounding Box:(4476, 1815, 8572, 5911)
(2) Bounding Box:(1214, 2757, 5310, 6853)
(3) Bounding Box:(2983, 4320, 7079, 8416)
(4) Bounding Box:(1867, 316, 5963, 4412)
(5) Bounding Box:(5003, 2400, 9099, 6496)
(6) Bounding Box:(6563, 5984, 10659, 10080)
(7) Bounding Box:(3892, 4681, 7988, 8777)
(8) Bounding Box:(5684, 168, 9780, 4264)
(9) Bounding Box:(6469, 436, 10565, 4532)
(10) Bounding Box:(2341, 3775, 6437, 7871)

>>> Completed
```

The script will also print out the minimum and maximum elevation values (in meters)
for the terrain which you you may want to take a note of for use within your game engine.

All converted heightmaps can be found in the `output/` directory. You can delete everything 
from `input/` and `output/` when you are finished.