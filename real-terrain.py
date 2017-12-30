# USGS elevation data: https://viewer.nationalmap.gov/basic/

import argparse
import datetime
import random
import re
import string
import sys
import subprocess

from PIL import Image

GDAL_INFO_BIN = 'bin/gdalinfo.exe'
GDAL_TRANSLATE_BIN = 'bin/gdal_translate.exe'
INPUT_DIR = 'input/'
OUTPUT_DIR = 'output/'

class HeightMap(object):
    def __init__(self, input_data, resolution):
        self.resolution = resolution
        self.input_data = INPUT_DIR + input_data
        self.raster_info = None
        self.min_elevation = None
        self.max_elevation = None
        self.output_full = None
        self.output_scaled = None
        self.main()

    def main(self):
        self._generate_heightmap_name()
        self._gdal_info()
        self._find_elevation_range()
        self._gdal_translate()
        self._scale_mode()
        self._crop_mode()

    def _generate_heightmap_name(self):
        timestamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S_')
        uid = ''.join(random.choice(string.ascii_lowercase) for i in range(4))
        self.output_full = OUTPUT_DIR + timestamp + uid + '_heightmap_full.png'
        self.output_scaled = OUTPUT_DIR + timestamp + uid + '_heightmap_scaled.png'
        self.output_cropped = OUTPUT_DIR + timestamp + uid

    def _gdal_info(self):
        gdal_info_cmd = [GDAL_INFO_BIN, '-stats', self.input_data]
        try:
            print('\n>>> Extracting elevation information from input data')
            self.raster_info = str(subprocess.check_output(gdal_info_cmd))
        except subprocess.CalledProcessError as exception:
            print("Failed to retrieve raster information:\n", exception.output)
            sys.exit(1)

    def _find_elevation_range(self):
        self.min_elevation = re.findall(r'(?<=STATISTICS_MINIMUM=)\-?\d{1,}',
                                        self.raster_info)[0]
        self.max_elevation = re.findall(r'(?<=STATISTICS_MAXIMUM=)\-?\d{1,}',
                                        self.raster_info)[0]
        print('Minimum elevation: {}m'.format(self.min_elevation))
        print('Maximum elevation: {}m'.format(self.max_elevation))
        print('Elevation range: {}m'.format(int(self.max_elevation) - int(self.min_elevation)))

    def _gdal_translate(self):
        gdal_translate_cmd = [GDAL_TRANSLATE_BIN, '-of', 'PNG', '-ot', 'UInt16', '-scale',
                              self.min_elevation, self.max_elevation, '0', '65535',
                              self.input_data, self.output_full]
        print('\n>>> Converting input data to full resolution 16-bit PNG')
        subprocess.call(gdal_translate_cmd)

    def _scale_mode(self):
        gdal_translate_cmd = [GDAL_TRANSLATE_BIN, '-outsize', self.resolution,
                              self.resolution, '-of', 'PNG', '-ot', 'UInt16', '-scale',
                              self.min_elevation, self.max_elevation, '0', '65535',
                              self.input_data, self.output_scaled]
        print('\n>>> Converting input data to scaled resolution 16-bit PNG')
        subprocess.call(gdal_translate_cmd)

    def _crop_mode(self):
        img = Image.open(self.output_full)
        width, height = img.size
        slice_size = int(self.resolution)

        print('\n>>> Slicing full resolution heightmap into tiles.')

        for y in range(0, height, slice_size):
            for x in range(0, width, slice_size):
                mx = min(x + slice_size, width)
                my = min(y + slice_size, height)
                img_slice = img.crop((x, y, mx, my))
                img_slice.save(self.output_cropped + "_heightmap_cropped_{}-{}.png".format(x, y))

def main():
    parser = argparse.ArgumentParser(description='Generate a 16-bit PNG ' \
                                                'heightmap from USGS raster data.')
    parser.add_argument('data', metavar='input-data',
                        help='File or folder name of the data located in the \'input\' folder which \
                              you would like to convert. File format must be one of IMG, ArcGrid or \
                              GeoTiff.')
    parser.add_argument('-r', metavar='output-resolution', type=str, default='4096',
                        help='Output resolution of the PNG heightmap. The default is 4096.')

    args = parser.parse_args()
    resolution = args.r
    input_data = args.data

    HeightMap(input_data=input_data, resolution=resolution)

    print('\n>>> Completed')

if __name__ == '__main__':
    main()
