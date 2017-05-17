# ENVI Image Band Difference

This task performs a difference analysis on a specific band in two images from the same sensor.

This task can be run with Python using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/)

### Table of Contents

- [Quickstart](#quickstart) - Get started!
- [Inputs](#inputs) - Required and optional task inputs.
- [Outputs](#outputs) - Task outputs and example contents.
- [Runtime](#runtime) - Example estimate of task runtime.
- [Advanced](#advanced) - Additional information for advanced users.
- [Contact Us](#contact-us) - Contact tech or document owner.

### Quickstart

Example Script: Run in a python environment (i.e. - IPython) using the gbdxtools interface.

```python
from gbdxtools import Interface
gbdx = Interface()

# Insert correct path to image in S3 location.
# Note: Images must have the same dimensions, have a single band, and from the same sensor. 
#   See Advanced script for example of end to end example.
data1 = 's3://gbd-customer-data/CustomerAccount#/PathToImage1/'
data2 = 's3://gbd-customer-data/CustomerAccount#/PathToImage2/'

envi_IBD = gbdx.Task("ENVI_ImageBandDifference")
envi_IBD.inputs.input_raster1 = data1
envi_IBD.inputs.input_raster2 = data2

workflow = gbdx.Workflow([envi_IBD])

workflow.savedata(
    envi_IBD.outputs.output_raster_uri,
    location='ImageBandDiff/output_raster_uri' # edit location to suit account
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```

### Inputs

The following table lists all inputs for this task. For details regarding the use of all ENVI input types refer to the [ENVI Task Runner Inputs](https://gbdxdocs.digitalglobe.com/docs/envi-task-runner-inputs) documentation.

| Name                        | Required | Default | Valid Values                             | Description                              |
| --------------------------- | :------: | ------- | ---------------------------------------- | ---------------------------------------- |
| file_types                  |  False   | None    | string                                   | GBDX Option. Comma separated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING |
| input_raster1               |   True   | None    | A valid S3 URL containing image files.   | Specify a single-band raster on which to perform an image difference of input band. -- Value Type: ENVIRASTER |
| input_raster1_format        |  False   | None    | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the format of the image, for example: landsat-8. -- Value Type: STRING |
| input_raster1_band_grouping |  False   | None    | [[See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md)](https://gbdxdocs.digitalglobe.com/docs/envi-task-runner-inputs) | Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING |
| input_raster1_filename      |  False   | None    | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING |
| input_raster2               |   True   | None    | A valid S3 URL containing image files.   | Specify a second single-band raster on which to perform an image difference of input band. -- Value Type: ENVIRASTER |
| input_raster2_format        |  False   | None    | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the format of the image, for example: landsat-8. -- Value Type: DICTIONARY |
| input_raster2_band_grouping |  False   | None    | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING |
| input_raster2_filename      |  False   | None    | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING |
| output_raster_uri_filename  |  False   | None    | string                                   | Specify a string with the fully-qualified path and filename for OUTPUT_RASTER. -- Value Type: STRING |

### Outputs

The following table lists all the tasks outputs.

| Name              | Required | Description                              |
| ----------------- | :------: | ---------------------------------------- |
| output_raster_uri |   True   | Output for OUTPUT_RASTER.                |
| task_meta_data    |  False   | GBDX Option. Output location for task meta data such as execution log and output JSON. |

##### Output Structure

The output_raster image file will be written to the specified S3 Customer Account Location in GeoTiff (\*.tif) format, with an ENVI header file (\*.hdr).



### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

| Sensor Name | Total Pixels | Total Area (k2) | Time(sec) | Time/Area k2 |
| ----------- | :----------: | --------------- | --------- | ------------ |
| WV02        | 31,754,708  | 480.820         | 168.474    | 0.35         |
| WV03        |  30,096,907 | 167.091       | 163.649   | 0.98     |
| GE01        | 28,492,530  | 312.104      |  165.061    |  0.53   |
|  QB02       | 22,635,330   | 321.188      |  170.367   |  0.53   |



### Advanced

```Python
from gbdxtools import Interface
gbdx = Interface()

# Insert correct path to image in S3 location.
# Images must have an intersection, otherwise the task will fail.
data1 = 's3://gbd-customer-data/CustomerAccount#/PathToImage1/'
data2 = 's3://gbd-customer-data/CustomerAccount#/PathToImage2/'

aoptask1 = gbdx.Task(
    "AOP_Strip_Processor",
    data=data1, 
    enable_acomp=True, 
    enable_pansharpen=False, 
    enable_dra=False, 
    bands='MS'
)

aoptask2 = gbdx.Task(
    "AOP_Strip_Processor",
    data=data2, 
    enable_acomp=True, 
    enable_pansharpen=False, 
    enable_dra=False, 
    bands='MS'
)

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
    envi_IBD.outputs.output_raster_uri,
    location='ImageBandDiff/output_raster_uri'
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```



### Background
For background on the development and implementation of ENVI_ImageBandDifference see [here](http://www.harrisgeospatial.com/docs/ImageChange.html#ICSettings).


### Contact
Document Owner - [Kathleen Johnson](kathleen.johnson@digitalglobe.com)
