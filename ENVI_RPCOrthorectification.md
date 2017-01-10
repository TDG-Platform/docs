### Description
This task orthorectifies an image georeferenced with RPCs using a DEM and optional GCPs. For more information on RPCOrthorectification see [Background on RPC Orthorectification](http://www.harrisgeospatial.com/docs/rpcbackground.html)

This task can be run with Python using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/)

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and output structure.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Issues](#issues) - Current or past known issues.
 * [Background](#background) - Background information.
 * [Contact](#contact) - Contact information.

### Quickstart
Quick start example.

```python

# Quickstart **Example Script Run in Python using the gbdxTools InterfaceExample producing a single band vegetation mask from a tif file.
# First Initialize the Environment

from gbdxtools import Interface
gbdx = Interface()
#Insert correct path to image in S3 location
image = "s3://gbd-customer-data/CustomerAccount#/PathToImage1/"
#Note: The dem_raster port is optional, and if it is missing, the task runner will use the GMTED2010.jp2
envi_RPCO = gbdx.Task("ENVI_RPCOrthorectification")
envi_RPCO.inputs.file_types = "tif"
envi_RPCO.inputs.input_raster = image

workflow = gbdx.Workflow([envi_RPCO])
workflow.savedata(
    envi_RPCO.outputs.output_raster_uri,
        location='ENVI_RPCO/results/'
)
workflow.execute()
status = workflow.status["state"]
wf_id = workflow.id
# print wf_id
# print status
```

### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
file_types|False|None| .hdr, .tif |GBDX Option. Comma seperated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING
input_raster|True|None| Image with associated RPC information e.g. IKONOS imagery |Specify a raster that is the RPC-based image to orthorectify. -- Value Type: ENVIRASTER
input_raster_metadata|False|None| |Provide a dictionary of attributes for overriding the raster metadata. -- Value Type: DICTIONARY
input_raster_band_grouping|False|None| A string name identify which band grouping to use for the task.[see supported datasets](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner.md#ENVIRPCRasterSpatialRef)|Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING
dem_is_height_above_ellipsoid|False|None| True/False|Set this property to true if the DEM is already expressed as the height above the ellipsoid and no geoid offset is required. -- Value Type: BOOL
output_subset|False|None| |Use this property to define a spatial subset from the input image that will apply to the output from ENVIRPCOrthorectificationTask. The output will be a rectangular subset that encompasses the the extent of the input subset. If you set this property, the output extent will be larger than that of the input subset, but the output may contain background pixels. Also, you do not need to specify the ENVIGCPSet::ApplyOffset method to adjust the position of ground control points (GCPs). Set this property to a four-element array expressing the spatial range (in pixels) of the input image. The array is of the form [x1, y1, x2, y2]. Pixel coordinates are zero-based. -- Value Type: INT[4]
input_gcp|False|None| |A set of ground control points (GCPs). -- Value Type: ENVIGCPSET
grid_spacing|False|None| |Grid spacing to use. -- Value Type: INT -- Default Value: 10
dem_raster|False|None| |Specify a digital elevation model (DEM) raster. It must have valid map information and the same spatial extent as INPUT_RASTER. Without elevation information from a DEM, RPCs only give an approximate geographic location. If you do not have a DEM file readily available, you can use the global DEM named GMTED2010.jp2 that is provided with your ENVI installation under the Exelis/envixx/data folder. The Global Multi-resolution Terrain Elevation Data 2010 (GMTED2010) dataset has a mean resolution of 30 arc seconds. -- Value Type: ENVIRASTER
dem_raster_metadata|False|None| |Provide a dictionary of attributes for overriding the raster metadata. -- Value Type: DICTIONARY
dem_raster_band_grouping|False|None|[see supported datasets](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner.md#ENVIRPCRasterSpatialRef) |Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING
geoid_offset|False|None| raster dependent|Set this property to a floating-point value (in meters) of a geoid offset if the DEM is referenced to mean sea level. -- Value Type: DOUBLE
resampling|False|None| see Description|Specify the resampling method.  Nearest Neighbor: Uses the nearest pixel without any interpolation.  Bilinear: Performs a linear interpolation using four pixels to resample, Cubic Convolution: Uses 16 pixels to approximate the sinc function using cubic polynomials to resample the image. -- Value Type: STRING -- Default Value: "Bilinear"
output_pixel_size|False|None| |Set this property to a two-element array indicating the output X and Y pixel size, in meters. The default value is the pixel size of the input image. -- Value Type: DOUBLE[2]
output_raster_uri_filename|False|None| s3 location with the name |Specify a string with the fully-qualified path and filename for OUTPUT_RASTER. -- Value Type: STRING

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
task_meta_data|False|None| |GBDX Option. Output location for task meta data such as execution log and output JSON
output_raster_uri|True|None| |Outputor OUTPUT_RASTER. -- Value Type: ENVIURI

**Output structure**

This task creates both a tif and hdr file of the input image following the ortho-rectification process.


### Advanced
Include example(s) with complicated parameter settings and/or example(s) where the task is used as part of a workflow involving other GBDX tasks.

```python

# The following script demonstrates the user defined DEM option rather than the default ENVI supplied DEM
# First Initialize the Environment
from gbdxtools import Interface
gbdx = Interface()
image = "s3://gbd-customer-data/CustomerAccount#/PathToImage/"
dem = "s3://gbd-customer-data/CustomerAccount#/PathToDEM/"

envi_RPCO = gbdx.Task("ENVI_RPCOrthorectification")
envi_RPCO.inputs.file_types = "tif"
envi_RPCO.inputs.input_raster = image
envi_RPCO.inputs.dem_raster = dem

workflow = gbdx.Workflow([envi_RPCO])
workflow.savedata(
    envi_RPCO.outputs.output_raster_uri,
        location='ENVI_RPCO/results/DEM'
)
workflow.execute()
status = workflow.status["state"]
wf_id = workflow.id
# print wf_id
# print status
```

### Issues
User specified DEM values must match the name of the image.


### Background
For background on the development and implementation of ENVI_RPCOrthorectification see [here](http://www.harrisgeospatial.com/docs/RPCOrthorectification.html).


### Contact
Document owner - Carl Reeder creeder@digitalglobe.com
