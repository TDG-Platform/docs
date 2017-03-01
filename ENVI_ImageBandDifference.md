### Description
This task performs a difference analysis on a specific band in two images.

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

Quick start example.

```python
# Quickstart example for ENVI_ImageBandDifference  
from gbdxtools import Interface
gbdx = Interface()

# Insert correct path to image in S3 location.
# Images must have an intersection, otherwise the task will fail.
NDVI1 = 's3://gbd-customer-data/CustomerAccount#/PathToImage1/'
NDVI2 = 's3://gbd-customer-data/CustomerAccount#/PathToImage2/'

envi_IBD = gbdx.Task("ENVI_ImageBandDifference")
envi_IBD.inputs.input_raster1 = NDVI1
envi_IBD.inputs.input_raster2 = NDVI2

workflow = gbdx.Workflow([envi_IBD])

workflow.savedata(
    envi_IBD.outputs.output_raster_uri,
    location='Benchmark/IBD'
)

workflow.execute()

# To monitor workflow, use the following command while
#  the Python interpreter is still open.
workflow.status
```

### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False). For more information on ENVI specific inputs [see ENVI Task Runner Inputs Inputs](https://gbdxdocs.digitalglobe.com/docs/envi-task-runner-inputs)

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
file_types|False|None| .hdr,.tif|GBDX Option. Comma separated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING
input_raster1|True|None| A valid S3 folder containing image files. |Specify a single-band raster on which to perform an image difference of input band. -- Value Type: ENVIRASTER
input_raster1_format|False|None| [More on ENVIRASTER input port](https://gbdxdocs.digitalglobe.com/docs/envi-task-runner-inputs)|Provide the format of the image, for example: landsat-8. -- Value Type: STRING
input_raster1_band_grouping|False|None| [More on ENVIRASTER input port](https://gbdxdocs.digitalglobe.com/docs/envi-task-runner-inputs)|Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING
input_raster1_filename|False|None| [More on ENVIRASTER input port](https://gbdxdocs.digitalglobe.com/docs/envi-task-runner-inputs) |Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING
input_raster2|True|None|  A valid S3 folder containing image files.  |Specify a second single-band raster on which to perform an image difference of input band. -- Value Type: ENVIRASTER
input_raster2_format|False|None| [More on ENVIRASTER input port](https://gbdxdocs.digitalglobe.com/docs/envi-task-runner-inputs)|Provide the format of the image, for example: landsat-8. -- Value Type: DICTIONARY
input_raster2_band_grouping|False|None| [More on ENVIRASTER input port](https://gbdxdocs.digitalglobe.com/docs/envi-task-runner-inputs)|Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING
input_raster2_filename|False|None| [More on ENVIRASTER input port](https://gbdxdocs.digitalglobe.com/docs/envi-task-runner-inputs) |Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING
output_raster_uri_filename|False|None| output_raster |Specify a string with the fully-qualified path and filename for OUTPUT_RASTER. -- Value Type: STRING

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Description  
--------|:----------:|-----------|---------------
task_meta_data|False|None| GBDX Option. Output location for task meta data such as execution log and output JSON
output_raster_uri|True|None| Output for OUTPUT_RASTER. -- Value Type: ENVIURI

**Output structure**

The output of this task is a single band raster of the difference between the two input raster datasets, in both ENVI standard format (including header file) and .tif format.

### Advanced
```Python
from gbdxtools import Interface
gbdx = Interface()

# Insert correct path to image in S3 location.
# Images must have an intersection, otherwise the task will fail.
data1 = 's3://gbd-customer-data/CustomerAccount#/PathToImage1/'
data2 = 's3://gbd-customer-data/CustomerAccount#/PathToImage2/'

aoptask1 = gbdx.Task("AOP_Strip_Processor",
    data=data1, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')
aoptask2 = gbdx.Task("AOP_Strip_Processor",
    data=data2, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')

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
envi_IBD.inputs.input_raster1 = envi_II.outputs.output_raster1_uri.value
envi_IBD.inputs.input_raster2 = envi_II.outputs.output_raster2_uri.value

workflow = gbdx.Workflow([aoptask1, aoptask2, envi_ndvi1, envi_ndvi2, envi_II, envi_IBD])

workflow.savedata(
    envi_II.outputs.output_raster1_uri,
    location='Benchmark/ENVI_ImageIntersection/fromNDVI'
)

workflow.savedata(
    envi_II.outputs.output_raster2_uri,
    location='Benchmark/ENVI_ImageIntersection/fromNDVI'
)

workflow.savedata(
    envi_IBD.outputs.output_raster_uri,
    location='Benchmark/ENVI_IBD/new'
)

workflow.execute()


# To monitor workflow, use the following command while
#  the Python interpreter is still open.
workflow.status
```


### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  | Total Pixels| Total Area (k2)  |  Time(min)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
WV02|73,005,420|292.02| 169.60| 0.74

### Issues
Processing of the images before running the task ENVI_ImageBandDifference may be required. Examples of image processing steps which may be useful prior to running this task are found in the advanced options.  

### Background
For background on the development and implementation of ENVI_ImageBandDifference see [here](http://www.harrisgeospatial.com/docs/ImageChange.html#ICSettings).


### Contact
Document Owner - Carl Reeder - creeder@digitalglobe.com
