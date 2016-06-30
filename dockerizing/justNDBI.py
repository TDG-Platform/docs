import osgeo.gdal as gdal
import struct
from gdalconst import *
import glob
import json
import os

# define filepath for L8 bands
filepath = "/mnt/work/input/image/"

# use any L8 band as a template for output raster, passing in raster size, number of bands, band type, transformation, and projection
get_rast =  glob.glob(filepath + "*B5.TIF.ovr")
rast_template = gdal.Open(get_rast[0], gdal.GA_ReadOnly)
driver = rast_template.GetDriver()

with open('/mnt/work/input/ports.json') as portsfile:
    ports_js = json.load(portsfile)
message= ports_js['message']

# create output directory and define output filepath
os.makedirs("/mnt/work/output/output")
os.chdir("/mnt/work/output/output")
id = get_rast[0].split("/")[-1].split("_")[0]
outfile = ("/mnt/work/output/output/" + id + "_NDBI.TIF")
# create output raster for calculations to be written to, set properties to those of raster template
calculated_index = driver.Create(outfile, rast_template.RasterXSize, rast_template.RasterYSize, 1, gdal.GDT_Float32)
geoTransform = rast_template.GetGeoTransform()
geoProjection = rast_template.GetProjection()
calculated_index.SetGeoTransform(geoTransform)
calculated_index.SetProjection(geoProjection)

# function -> if/then index calculation (NDVI, NDBI, EBBI, NBAI)
# steps: retrieve bands, open bands, read in raster 1 line at a time using ReadRaster(x offset, y offset, x size, y size,
#   x buffer size (of raster being read to, change buffer size to upsample or downsample), y buffer size, type), unpack resulting
#   binary data into a tuple, calculate metric cell by cell, pack and add each calculated value to list, write list (one
#   line of raster) to output raster
def calculate_index():
    num_lines = rast_template.RasterYSize

    get_nir = glob.glob(filepath + "*B5.TIF.ovr")
    open_nir = gdal.Open(get_nir[0], gdal.GA_ReadOnly)
    nir_band = open_nir.GetRasterBand(1)

    get_swir6 = glob.glob(filepath + "*B6.TIF.ovr")
    open_swir6 = gdal.Open(get_swir6[0], gdal.GA_ReadOnly)
    swir6_band = open_swir6.GetRasterBand(1)

    for line in range(num_lines):
        output_line = ''

        nir_scanline = nir_band.ReadRaster(0, line, nir_band.XSize, 1, nir_band.XSize, 1, gdal.GDT_Float32)
        nir_tuple = struct.unpack("f" * nir_band.XSize, nir_scanline)

        swir6_scanline = swir6_band.ReadRaster(0, line, swir6_band.XSize, 1, swir6_band.XSize, 1, gdal.GDT_Float32)
        swir6_tuple = struct.unpack("f" * swir6_band.XSize, swir6_scanline)

        for i in range(len(nir_tuple)):
            upper = swir6_tuple[i] - nir_tuple[i]
            lower = swir6_tuple[i] + nir_tuple[i]
            if lower != 0:
                ndbi = upper / lower
            else:
                ndbi = 0
            output_line += struct.pack("f", ndbi)
        calculated_index.GetRasterBand(1).WriteRaster(0, line, nir_band.XSize, 1, output_line,
                                                                  buf_xsize=nir_band.XSize, buf_ysize=1,
                                                                  buf_type=gdal.GDT_Float32)
        del output_line

calculate_index()

# a status file always needs to be present to populate with the operation status
status = {}
status['status'] = 'Success'
status['reason'] = message

# write the json status
with open('/mnt/work/status.json', 'w') as statusfile:
        json.dump(status,statusfile)
