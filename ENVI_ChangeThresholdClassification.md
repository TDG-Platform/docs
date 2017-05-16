# ENVI Change Threshold Classification

### Description
This task lets you manually set the threshold needed to classify change detection between two images.

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

# Edit the following path to reflect a specific path to an image
NDVI1 = 's3://gbd-customer-data/CustomerAccount#/PathToImage1/'
NDVI2 = 's3://gbd-customer-data/CustomerAccount#/PathToImage2/'

envi_IBD = gbdx.Task("ENVI_ImageBandDifference")
envi_IBD.inputs.input_raster1 = NDVI1
envi_IBD.inputs.input_raster2 = NDVI2

envi_CTC = gbdx.Task("ENVI_ChangeThresholdClassification")
envi_CTC.inputs.input_raster = envi_IBD.outputs.output_raster_uri.value

workflow = gbdx.Workflow([envi_IBD, envi_CTC])

workflow.savedata(
    envi_CTC.outputs.output_raster_uri,
        location='ChangeThresh/output_raster_uri'
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```



### Inputs

The following table lists all inputs for this task. For details regarding the use of all ENVI input types refer to the [ENVI Task Runner Inputs]([See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md)) documentation.

| Name                       | Required | Default |               Valid Values               | Description                              |
| -------------------------- | :------: | :-----: | :--------------------------------------: | ---------------------------------------- |
| input_raster               |   True   |  None   |  A valid S3 URL containing image files.  | Specify a raster from which to run the task. -- Value Type: ENVIRASTER |
| input_raster_format        |  False   |  None   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the format of the image, for example: landsat-8. -- Value Type: STRING |
| input_raster_band_grouping |  False   |  None   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING |
| input_raster_filename      |  False   |  None   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING |
| increase_threshold         |  False   |  None   | string double (Threshold must match values within the input rasters) | Specify the increase threshold to show areas of increase. -- Value Type: DOUBLE |
| decrease_threshold         |  False   |  None   | string double (Threshold must match values within the input rasters) | Specify the decrease threshold to show areas of decrease. -- Value Type: DOUBLE |
| output_raster_uri_filename |  False   |  None   |                  string                  | Specify a string with the fully-qualified path and filename for OUTPUT_RASTER. -- Value Type: STRING |



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
| WV02        | 31,754,708  | 292.02       |  158.564   | 0.74     |
| Wv03        |  30,096,907 | 167.091      |  159.431   | 0.98     |
| GE01        | 28,492,530  | 165.061      |  157.986   |  0.53    |
| QB02        | 22,635,330  | 170.367      |  161.711   |  0.54    |


### Advanced

This task will take two multispectral images, which share geo-spatial extent, as input.  This example workflow includes the following ENVI tasks to prepare the images for the Change Threshold Classification task: Spectral Index, Image Intersection, and Image Band Difference.  Input rasters for the Change Threshold Classification task may be any  set of 1 band rasters sharing the same extent, spatial reference and pixel value format (e.g. Normalized Difference Vegetation Index)

```python
from gbdxtools import Interface
gbdx = Interface()

# Edit the following path to reflect a specific path to an image
data1 = 's3://gbd-customer-data/CustomerAccount#/PathToImage1/'
data2 = 's3://gbd-customer-data/CustomerAccount#/PathToImage2/'

aoptask1 = gbdx.Task("AOP_Strip_Processor") 
aoptask1.inputs.data = data
aoptask1.inputs.enable_dra = False
aoptask1.inputs.bands = 'MS'

aoptask2 = gbdx.Task("AOP_Strip_Processor") 
aoptask2.inputs.data = data
aoptask2.inputs.enable_dra = False
aoptask2.inputs.bands = 'MS'

envi_ndvi1 = gbdx.Task("ENVI_SpectralIndex")
envi_ndvi1.inputs.input_raster = aoptask1.outputs.data.value
envi_ndvi1.inputs.index = "Normalized Difference Vegetation Index"

envi_ndvi2 = gbdx.Task("ENVI_SpectralIndex")
envi_ndvi2.inputs.input_raster = aoptask2.outputs.data.value
envi_ndvi2.inputs.index = "Normalized Difference Vegetation Index"

envi_II = gbdx.Task("ENVI_ImageIntersection")
envi_II.inputs.input_raster1 = envi_ndvi1.outputs.output_raster_uri.value
envi_II.inputs.input_raster2 = envi_ndvi2.outputs.output_raster_uri.value

envi_IBD = gbdx.Task("ENVI_ImageBandDifference")
envi_IBD.inputs.input_raster1 = envi_II.outputs.output_raster1_uri.value
envi_IBD.inputs.input_raster2 = envi_II.outputs.output_raster2_uri.value

envi_CTC = gbdx.Task("ENVI_ChangeThresholdClassification")
envi_CTC.inputs.increase_threshold = "0.1"
envi_CTC.inputs.decrease_threshold = "0.5"
envi_CTC.inputs.input_raster = envi_IBD.outputs.output_raster_uri.value


workflow = gbdx.Workflow([
    aoptask1, aoptask2, envi_ndvi1, envi_ndvi2, envi_II, envi_IBD, envi_CTC
])

workflow.savedata(
    envi_CTC.outputs.output_raster_uri,
    location='ChangeThres/output_raster_uri' # edit location to suit account
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```


### Issues
Input rasters for the ENVI_ChangeThresholdClassification task will require pre-processing to fit specific input requirements.


### Background
For background on the development and implementation of ENVI Change Threshold Classification see [here](http://www.harrisgeospatial.com/docs/ENVIChangeThresholdClassificationTask.html).


### Contact
Document owner - [Kathleen Johnson](#kathleen.johnson@digitalglobe.com)
