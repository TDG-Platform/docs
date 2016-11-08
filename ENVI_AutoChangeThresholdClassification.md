# ENVI_AutoChangeThresholdClassification

### Description
This task uses pre-defined thresholding techniques to automatically classify change detection between two images

This task can be run with Python using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/)

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and output structure.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Runtime](#runtime) - Example estimate of task runtime.
 * [Issues](#issues) - Current or past known issues.
 * [Background](#background) - Background information.
 * [Contact](#contact) - Contact information.

### Quickstart

```python

from gbdxtools import Interface
gbdx = Interface()

NDVI1 = "s3://gbd-customer-data/cutomer_bucket/folder_name_with_image1"
NDVI2 = "s3://gbd-customer-data/cutomer_bucket/folder_name_with_image2"

envi_IBD = gbdx.Task("ENVI_ImageBandDifference")
envi_IBD.inputs.file_types = "tif"
envi_IBD.inputs.input_raster1 = NDVI1
envi_IBD.inputs.input_raster2 = NDVI2

envi_ACTC = gbdx.Task("ENVI_AutoChangeThresholdClassification")
envi_ACTC.inputs.threshold_method = "Kapur"
envi_ACTC.inputs.file_types = "tif"
envi_ACTC.inputs.input_raster = envi_IBD.outputs.output_raster_uri.value


workflow = gbdx.Workflow([envi_IBD, envi_ACTC])

workflow.savedata(
    envi_IBD.outputs.output_raster_uri,
        location='ENVI_ACTC/IBD'
)


workflow.savedata(
    envi_ACTC.outputs.output_raster_uri,
        location='ENVI_ACTC/IBD/ACTC/kapur'
)

workflow.execute()

status = workflow.status["state"]
wf_id = workflow.id

```

### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
file_types|False|None| .hdr,.tif|GBDX Option. Comma separated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING
input_raster|True|None| |requires two rasters to detect change, (input_raster1, input_raster2)|Specify two rasters on which to threshold. -- Value Type: ENVIRASTER
change_type|False|Both| The type of change to consider for change of interest -- Value Type: STRING
threshold_method|False|Otsu|"Otsu","Tsai","Kapur", "Kittler" |Specify the thresholding method. -- Value Type: STRING
output_raster_uri_filename|False|None|e.g. "ChangeThresholdClassification" |Outputor OUTPUT_RASTER. -- Value Type: ENVIURI

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
task_meta_data|False|None| |GBDX Option. Output location for task meta data such as execution log and output JSON
output_raster_uri|True|None|s3 Location for output raster |Outputor OUTPUT_RASTER. -- Value Type: ENVIURI

**Output structure**

The output of the Change Threshold Classification task is a single band raster in both .hdr and .tif format.  Based on the thresholds selected for change (increase/decrease) the image will show increases in pixel values in blue, and decreases in red.


### Advanced
This task will take two multispectral images, which share geo-spatial extent, as input.  This example workflow includes the following ENVI tasks to prepare the images for the Change Threshold Classification task: Spectral Index, Image Intersection, and Image Band Difference.  Input rasters for the Change Threshold Classification task may be any  set of 1 band rasters sharing the same extent, spatial reference and pixel value format (e.g. Normalized Difference Vegetation Index)

```python
from gbdxtools import Interface
gbdx = Interface()

data1 = "s3://receiving-dgcs-tdgplatform-com/Image_location"
data2 = "s3://receiving-dgcs-tdgplatform-com/Image_location"


aoptask1 = gbdx.Task("AOP_Strip_Processor", data=data1, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')
aoptask2 = gbdx.Task("AOP_Strip_Processor", data=data2, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')


envi_ndvi1 = gbdx.Task("ENVI_SpectralIndex")
envi_ndvi1.inputs.input_raster = aoptask1.outputs.data.value
envi_ndvi1.inputs.file_types = "hdr"
envi_ndvi1.inputs.index = "Normalized Difference Vegetation Index"

envi_ndvi2 = gbdx.Task("ENVI_SpectralIndex")
envi_ndvi2.inputs.input_raster = aoptask2.outputs.data.value
envi_ndvi2.inputs.file_types = "hdr"
envi_ndvi2.inputs.index = "Normalized Difference Vegetation Index"

envi_II = gbdx.Task("ENVI_ImageIntersection")
envi_II.inputs.file_types = "hdr"
envi_II.inputs.input_raster1 = envi_ndvi1.outputs.output_raster_uri.value
envi_II.inputs.input_raster2 = envi_ndvi2.outputs.output_raster_uri.value
envi_II.inputs.output_raster1_uri_filename = "NDVI1"
envi_II.inputs.output_raster2_uri_filename = "NDVI2"


envi_IBD = gbdx.Task("ENVI_ImageBandDifference")
envi_IBD.inputs.file_types = "hdr"
envi_IBD.inputs.input_raster1 = envi_II.outputs.output_raster1_uri.value
envi_IBD.inputs.input_raster2 = envi_II.outputs.output_raster2_uri.value

envi_ACTC = gbdx.Task("ENVI_AutoChangeThresholdClassification")
envi_ACTC.inputs.threshold_method = "Kapur"
envi_ACTC.inputs.file_types = "tif"
envi_ACTC.inputs.input_raster = envi_IBD.outputs.output_raster_uri.value


workflow = gbdx.Workflow([aoptask1, aoptask2, envi_ndvi1, envi_ndvi2, envi_II, envi_IBD, envi_ACTC])

workflow.savedata(
    envi_II.outputs.output_raster1_uri,
        location='ENVI_ImageIntersection/fromNDVI'
)

workflow.savedata(
    envi_II.outputs.output_raster2_uri,
        location='ENVI_ImageIntersection/fromNDVI'
)

workflow.savedata(
    envi_ACTC.outputs.output_raster_uri,
        location='ENVI_ACTC/NDVI_threshold'
)

workflow.execute()

status = workflow.status["state"]
wf_id = workflow.id

```
### Issues
Input rasters for the ENVI_AutoChangeThresholdClassification task will require pre-processing to fit specific input requirements.  Auto threshold may also require experimentation and iteration to find an acceptable threshold method (e.g. Kapur may not be the ideal method for a given raster dataset)


### Background
For background on the development and implementation of ENVI_ChangeThresholdClassification see [here](http://www.harrisgeospatial.com/docs/ENVIAutoChangeThresholdClassificationTask.html).


### Contact
Document owner - Carl Reeder creeder@digitalglobe.com
