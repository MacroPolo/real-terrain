# USGS elevation data: https://viewer.nationalmap.gov/basic/

import argparse
import datetime
import random
import re
import string
import sys
import subprocess

from PIL import Image

# We are dealing with large files here, so increase the DecompressionBombWarning threshold
Image.MAX_IMAGE_PIXELS = 1500000000

GDAL_INFO = 'bin/gdalinfo.exe'
GDAL_TRANSLATE = 'bin/gdal_translate.exe'
INPUT_DIR = 'input/'
OUTPUT_DIR = 'output/'

class HeightMap(object):
    def __init__(self, dem, scale=None, tile=None, tile_random=None):
        self.dem = INPUT_DIR + dem
        self.res_scale = scale
        self.res_tile = tile
        self.res_tile_random = tile_random

        self.min_elevation = None
        self.max_elevation = None
        self.output_full = None
        self.output_scale = None
        self.output_tile = None
        self.output_tile_random = None

        self.main()

    def main(self):
        self._generate_filenames()
        self._find_elevation_range()
        self._generate_full()
        if self.res_scale:
            self._generate_scale()
        if self.res_tile:
            self._generate_tile()
        if self.res_tile_random:
            self._generate_random()

    def _generate_filenames(self):
        timestamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S_')
        uid = ''.join(random.choice(string.ascii_lowercase) for i in range(4))
        self.output_full = OUTPUT_DIR + timestamp + uid + '_heightmap_full.png'
        self.output_scale = OUTPUT_DIR + timestamp + uid + '_heightmap_scaled.png'
        self.output_tile = OUTPUT_DIR + timestamp + uid

    def _find_elevation_range(self):
        gdal_info_cmd = [GDAL_INFO, '-stats', self.dem]
        try:
            print('\n>>> Extracting elevation information from input DEM.')
            raster_info = str(subprocess.check_output(gdal_info_cmd))
        except subprocess.CalledProcessError as exception:
            print("Failed to retrieve elevation information:\n", exception.output)
            sys.exit(1)

        self.min_elevation = re.findall(r'(?<=STATISTICS_MINIMUM=)\-?\d{1,}', raster_info)[0]
        self.max_elevation = re.findall(r'(?<=STATISTICS_MAXIMUM=)\-?\d{1,}', raster_info)[0]

        print('Minimum elevation: {}m'.format(self.min_elevation))
        print('Maximum elevation: {}m'.format(self.max_elevation))
        print('Elevation range: {}m'.format(int(self.max_elevation) - int(self.min_elevation)))

    def _generate_full(self):
        gdal_translate_cmd = [GDAL_TRANSLATE, '-of', 'PNG', '-ot', 'UInt16', '-scale',
                              self.min_elevation, self.max_elevation, '0', '65535',
                              self.dem, self.output_full]
        print('\n>>> Converting input DEM to full resolution 16-bit PNG.')
        subprocess.call(gdal_translate_cmd)

    def _generate_scale(self):
        gdal_translate_cmd = [GDAL_TRANSLATE, '-outsize', self.res_scale,
                              self.res_scale, '-of', 'PNG', '-ot', 'UInt16', '-scale',
                              self.min_elevation, self.max_elevation, '0', '65535',
                              self.dem, self.output_scale]
        print('\n>>> Converting input data to scaled resolution 16-bit PNG')
        subprocess.call(gdal_translate_cmd)

    def _generate_tile(self):
        img = Image.open(self.output_full)
        width, height = img.size
        tile_size = int(self.res_tile)

        print('\n>>> Slicing full resolution heightmap into sequential tiles.')

        for y in range(0, height, tile_size):
            for x in range(0, width, tile_size):
                mx = min(x + tile_size, width)
                my = min(y + tile_size, height)
                img_slice = img.crop((x, y, mx, my))
                img_slice.save(self.output_tile + "_heightmap_tile_{}-{}.png".format(x, y))

    def _generate_random(self):
        img = Image.open(self.output_full)
        width, height = img.size
        tile_size = int(self.res_tile_random)

        print('\n>>> Slicing full resolution heightmap into random tiles.')
        
        number_of_tiles = 10

        for i in range(number_of_tiles):
            x0 = random.randint(0, width - tile_size)
            y0 = random.randint(0, height - tile_size)
            x1 = x0 + tile_size
            y1 = y0 + tile_size
            print('({}) Bounding Box:{}'.format(i + 1, (x0, y0, x1, y1)))
            img_slice = img.crop((x0, y0, x1, y1))
            img_slice.save(self.output_tile + "_heightmap_random_{}.png".format(i))

def main():
    parser = argparse.ArgumentParser(description='Generate 16-bit PNG heightmaps from geospatial \
                                                  DEM files (IMG, GeoTiff and ArcGrid).')
    parser.add_argument('dem', metavar='dem',
                        help='File (IMG, GeoTiff) or folder (ArcGrid) name of the source data \
                              located in \'input\\\' which you would like to convert.')
    parser.add_argument('-s', metavar='scale', type=str,
                        help='Scale the full resolution heighmap to a fixed resolution.')
    parser.add_argument('-t', metavar='tile', type=str,
                        help='Slice the full resolution heighmap into sequential tiles.')
    parser.add_argument('-r', metavar='random', type=str,
                        help='Slice the full resolution heighmap into random tiles.')

    args = parser.parse_args()
    dem = args.dem
    scale = args.s
    tile = args.t
    tile_random = args.r

    HeightMap(dem=dem, scale=scale, tile=tile, tile_random=tile_random)

    print('\n>>> Completed')

if __name__ == '__main__':
    main()
