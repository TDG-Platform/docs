# ENVI_ImageIntersection

### Description
Image intersection takes two rasters as input, and it outputs two rasters that cover only the overlapping area of two inputs. If the input rasters have different projections or pixel sizes, one of the output rasters will be reprojected or resampled so that the two output rasters have the same number of samples and lines. File inputs can have standard map projections, can be pixel-based, or can have RPC information.

This task can be run with Python using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/)

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and output structure.
 * [Runtime](#runtime) - Example estimate of task runtime.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Issues](#issues) - Current or past known issues.
 * [Contact](#contact) - Contact information.

### Quickstart
Quick start example.

```python
# First Initialize the Environment
from gbdxtools import Interface
gbdx = Interface()

#Edit the following path to reflect a specific path to an image

data1 = 's3://gbd-customer-data/CustomerAccount#/PathToImage1/'
data2 = 's3://gbd-customer-data/CustomerAccount#/PathToImage2/'

aoptask1 = gbdx.Task("AOP_Strip_Processor", data=data1, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')
aoptask2 = gbdx.Task("AOP_Strip_Processor", data=data2, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')

envi_II = gbdx.Task("ENVI_ImageIntersection")
envi_II.inputs.input_raster1 = data1
envi_II.inputs.input_raster2 = data2
envi_II.inputs.output_raster1_uri_filename = "Image1"
envi_II.inputs.output_raster2_uri_filename = "Image2"

workflow = gbdx.Workflow([aoptask1, aoptask2, envi_II])

workflow.savedata(
    envi_II.outputs.output_raster1_uri,
        location='ENVI_ImageIntersection/image1'
)
workflow.savedata(
    envi_II.outputs.output_raster2_uri,
        location='ENVI_ImageIntersection/image2'
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
warping_method|False|Triangulation|"Polynomial", "Rigorous", "Triangulation" |Specify the warping method to use. -- Value Type: STRING -- Default Value: "Triangulation"
resampling|False|None|Nearest Neighbor, Bilinear, Cubic Convolution |Specify the resampling method.  Nearest Neighbor: Uses the nearest pixel without any interpolation.  Bilinear: Performs a linear interpolation using four pixels to resample, Cubic Convolution: Uses 16 pixels to approximate the sinc function using cubic polynomials to resample the image. -- Value Type: STRING -- Default Value: "Bilinear"
input_raster1|True|None| |Specify a raster to use as the base for computing the intersection. -- Value Type: ENVIRASTER
input_raster1_format  |	False  |       N/A   |	string  |	A string for selecting the format for raster1 (non-DG format). Please refer to Supported Datasets table below for a list of valid values for currently supported image data products.
input_raster1_band_grouping    |	False  |    N/A	|   string   |	A string name indentify which band grouping to use for the task.
input_raster1_filename    |  False   |   N/A    | string   |  Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner.
input_raster2|True|None| |Specify a second raster for computing the intersection. -- Value Type: ENVIRASTER
input_raster2_format  |	False  |       N/A   |	string  |	A string for selecting the format for raster 2 (non-DG format). Please refer to Supported Datasets table below for a list of valid values for currently supported image data products.
input_raster2_band_grouping    |	False  |    N/A	|   string   |	A string name indentify which band grouping to use for the task.
input_raster2_filename    |  False   |   N/A    | string   |  Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner.


### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
task_meta_data|False|None| |GBDX Option. Output location for task meta data such as execution log and output JSON
output_raster2_uri|True|None| |Output or OUTPUT_RASTER2. -- Value Type: ENVIURI
output_raster2_uri_filename|False|None| |Output or OUTPUT_RASTER2. -- Value Type: ENVIURI
output_raster1_uri|True|None| |Outpu tor OUTPUT_RASTER1. -- Value Type: ENVIURI
output_raster1_uri_filename|False|None| |Output OUTPUT_RASTER1. -- Value Type: ENVIURI

**Output structure**

The output of this task will be two rasters (output_raster1 and output_raster2) rezised to the shared extent or overlap of the rasters.


### Runtime

The following table lists runtime outputs for applicable sensors.
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Total Pixels  |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB | 638,471,053| 638.5| 1135.43 | 1.78|
WV01|1,431,417,804|715.5| 636.82 | 0.89|
WV02|638,471,053|1276.9| 407.27 | 0.32|
WV03|260,999,184|391|383.55|0.98|
GE| 350,236,670|577.8|697.86| 1.21|

### Advanced
This task will take two multispectral images, which share geo-spatial extent, as input.  This example workflow includes the following ENVI tasks to prepare the images for the Change Threshold Classification task: Spectral Index, Image Intersection, and Image Band Difference.  Input rasters for the Change Threshold Classification task may be any  set of 1 band rasters sharing the same extent, spatial reference and pixel value format (e.g. Normalized Difference Vegetation Index)

```python

from gbdxtools import Interface
gbdx = Interface()

#Edit the following path to reflect a specific path to an image
data1 = 's3://gbd-customer-data/CustomerAccount#/PathToImage1/'
data2 = 's3://gbd-customer-data/CustomerAccount#/PathToImage2/'

aoptask1 = gbdx.Task("AOP_Strip_Processor", data=data1, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')
aoptask2 = gbdx.Task("AOP_Strip_Processor", data=data2, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')

# Capture AOP task outputs
#orthoed_output = aoptask.get_output('data')

envi_ndvi1 = gbdx.Task("ENVI_SpectralIndex")
envi_ndvi1.inputs.input_raster = aoptask1.outputs.data.value
envi_ndvi1.inputs.index = "Normalized Difference Vegetation Index"

envi_ndvi2 = gbdx.Task("ENVI_SpectralIndex")
envi_ndvi2.inputs.input_raster = aoptask2.outputs.data.value
envi_ndvi2.inputs.index = "Normalized Difference Vegetation Index"

envi_II = gbdx.Task("ENVI_ImageIntersection")
envi_II.inputs.input_raster1 = envi_ndvi1.outputs.output_raster_uri.value
envi_II.inputs.input_raster2 = envi_ndvi2.outputs.output_raster_uri.value
envi_II.inputs.output_raster1_uri_filename = "NDVI1"
envi_II.inputs.output_raster2_uri_filename = "NDVI2"


envi_IBD = gbdx.Task("ENVI_ImageBandDifference")
envi_IBD.inputs.file_types = "hdr"
envi_IBD.inputs.input_raster1 = envi_II.outputs.output_raster1_uri.value
envi_IBD.inputs.input_raster2 = envi_II.outputs.output_raster2_uri.value

envi_CTC = gbdx.Task("ENVI_ChangeThresholdClassification")
envi_CTC.inputs.increase_threshold = "0.1"
envi_CTC.inputs.decrease_threshold = "0.5"
envi_CTC.inputs.file_types = "hdr"
envi_CTC.inputs.input_raster = envi_IBD.outputs.output_raster_uri.value


workflow = gbdx.Workflow([aoptask1, aoptask2, envi_ndvi1, envi_ndvi2, envi_II, envi_IBD, envi_CTC])

#Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
workflow.savedata(
    envi_II.outputs.output_raster1_uri,
        location='ENVI_ImageIntersection/fromNDVI'
)

workflow.savedata(
    envi_II.outputs.output_raster2_uri,
        location='ENVI_ImageIntersection/fromNDVI'
)

workflow.savedata(
    envi_CTC.outputs.output_raster_uri,
        location='ENVI_CTC/NDVI_threshold'
)

workflow.execute()

status = workflow.status["state"]
wf_id = workflow.id

```
### Issues
Currently the advanced options for the task and the task in the gbdx webapp are not available because of the requirement of multiple input parameters.


### Background
For background on the development and implementation of ENVI_ImageIntersection see [here](http://www.harrisgeospatial.com/docs/ENVIImageIntersectionTask.html).


### Contact
Document Owner - [Kathleen Johnson](kathleen.johnson@digitalglobe.com)
