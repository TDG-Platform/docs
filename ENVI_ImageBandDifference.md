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
# Quickstart example for ENVI_ImageBandDifference:0.0.2.  
from gbdxtools import Interface
gbdx = Interface()

#Insert correct path to image in S3 location
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

status = workflow.status["state"]
wf_id = workflow.id
```

### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
file_types|False|None| |GBDX Option. Comma seperated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING
input_raster1|True|None| |Specify a single-band raster on which to perform an image difference of input band. -- Value Type: ENVIRASTER
input_raster1_metadata|False|None| |Provide a dictionary of attributes for overriding the raster metadata. -- Value Type: DICTIONARY
input_raster1_band_grouping|False|None| |Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING
input_raster1_filename|False|None| |Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING
input_raster2|True|None| |Specify a second single-band raster on which to perform an image difference of input band. -- Value Type: ENVIRASTER
input_raster2_metadata|False|None| |Provide a dictionary of attributes for overriding the raster metadata. -- Value Type: DICTIONARY
input_raster2_band_grouping|False|None| |Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING
input_raster2_filename|False|None| |Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING
output_raster_uri_filename|False|None| |Specify a string with the fully-qualified path and filename for OUTPUT_RASTER. -- Value Type: STRING

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
task_meta_data|False|None| |GBDX Option. Output location for task meta data such as execution log and output JSON
output_raster_uri|True|None| |Output for OUTPUT_RASTER. -- Value Type: ENVIURI

**Output structure**

Explain output structure via example.


### Advanced
Include example(s) with complicated parameter settings and/or example(s) where
ENVI_ImageBandDifference:0.0.2 is used as part of a workflow involving other GBDX tasks.
```Python
from gbdxtools import Interface
gbdx = Interface()

#Insert correct path to image in S3 location
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
#envi_II.outputs.output_raster1_uri = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/ENVI_ImageIntersection/fromNDVI1"
#envi_II.outputs.output_raster2_uri = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/ENVI_ImageIntersection/fromNDVI2"

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

status = workflow.status["state"]
wf_id = workflow.id
```


### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Total Area (k2)  |  Time(min)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
WV02|73,005,420|292.02| 169.60| 0.74

### Issues
Processing of the images before running the task ENVI_ImageBandDifference may be required. Examples of image processing steps which may be useful prior to running this task are found in the advanced options.  

### Background
For background on the development and implementation of ENVI_ImageBandDifference:0.0.2 see [here](https://www.harrisgeospatial.com/docs/ImageChangeTutorial.html).


### Contact
Document Owner - Carl Reeder - creeder@digitalglobe.com
