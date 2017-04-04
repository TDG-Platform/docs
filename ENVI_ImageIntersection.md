# ENVI Image Intersection

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

Example Script: Run in a python environment (i.e. - IPython) using the gbdxtools interface.

```python
from gbdxtools import Interface
gbdx = Interface()

# Edit the following path to reflect a specific path to an image
data1 = 's3://gbd-customer-data/CustomerAccount#/PathToImage1/'
data2 = 's3://gbd-customer-data/CustomerAccount#/PathToImage2/'

envi_II = gbdx.Task("ENVI_ImageIntersection")
envi_II.inputs.input_raster1 = data1
envi_II.inputs.input_raster2 = data2

workflow = gbdx.Workflow([ envi_II ])

workflow.savedata(
    envi_II.outputs.output_raster1_uri,
        location='ImageIntersection/output_raster1_uri'
)
workflow.savedata(
    envi_II.outputs.output_raster2_uri,
        location='ImageIntersection/output_raster2_uri'
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```



### Inputs

The following table lists all inputs for this task. For details regarding the use of all ENVI input types refer to the [ENVI Task Runner Inputs]([See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md)) documentation.

| Name                        | Required | Default         | Valid Values                             | Description                              |
| --------------------------- | :------: | --------------- | ---------------------------------------- | ---------------------------------------- |
| input_raster1               |   True   | None            | A valid S3 URL containing image files.   | Specify a raster from which to run the task. -- Value Type: ENVIRASTER |
| input_raster1_format        |  False   | None            | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the format of the image, for example: landsat-8. -- Value Type: STRING |
| input_raster1_band_grouping |  False   | None            | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING |
| input_raster1_filename      |  False   | None            | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING |
| input_raster2               |   True   | None            | A valid S3 URL containing image files.   | Specify a raster from which to run the task. -- Value Type: ENVIRASTER |
| input_raster2_format        |  False   | None            | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the format of the image, for example: landsat-8. -- Value Type: STRING |
| input_raster2_band_grouping |  False   | None            | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING |
| input_raster2_filename      |  False   | None            | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING |
| resampling                  |  False   | 'Bilinear'      | 'Nearest Neighbor', 'Bilinear', 'Cubic Convolution' | Specify the resampling method.  Nearest Neighbor: Uses the nearest pixel without any interpolation.  Bilinear: Performs a linear interpolation using four pixels to resample, Cubic Convolution: Uses 16 pixels to approximate the sinc function using cubic polynomials to resample the image. -- Value Type: STRING |
| warping_method              |  False   | 'Triangulation' | 'Polynomial', 'Rigorous', 'Triangulation' | Specify the warping method to use. -- Value Type: STRING |
| output_raster1_uri_filename |  False   | None            | string                                   | Specify a string with the fully-qualified path and filename for OUTPUT_RASTER. -- Value Type: STRING |
| output_raster2_uri_filename |  False   | None            | string                                   | Specify a string with the fully-qualified path and filename for OUTPUT_RASTER. -- Value Type: STRING |



### Outputs

The following table lists all the tasks outputs.

| Name               | Required | Description                              |
| ------------------ | :------: | ---------------------------------------- |
| output_raster1_uri |   True   | Output for OUTPUT_RASTER1.               |
| output_raster2_uri |   True   | Output for OUTPUT_RASTER2.               |
| task_meta_data     |  False   | GBDX Option. Output location for task meta data such as execution log and output JSON. |

##### Output Structure

The output_raster image file will be written to the specified S3 Customer Account Location in GeoTiff (\*.tif) format, with an ENVI header file (\*.hdr).




### Runtime

The following table lists runtime outputs for applicable sensors.
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

| Sensor Name | Total Pixels  | Total Area (k2) | Time(secs) | Time/Area k2 |
| ----------- | :-----------: | --------------- | ---------- | ------------ |
| QB          |  638,471,053  | 638.5           | 1135.43    | 1.78         |
| WV01        | 1,431,417,804 | 715.5           | 636.82     | 0.89         |
| WV02        |  638,471,053  | 1276.9          | 407.27     | 0.32         |
| WV03        |  260,999,184  | 391             | 383.55     | 0.98         |
| GE          |  350,236,670  | 577.8           | 697.86     | 1.21         |



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
    envi_IBD.outputs.output_raster1_uri,
    location='ImgIntersect/output_raster1_uri' # edit location to suit account
)

workflow.savedata(
    envi_IBD.outputs.output_raster2_uri,
    location='ImgIntersect/output_raster2_uri' # edit location to suit account
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```
### Issues
Currently the advanced options for the task and the task in the gbdx webapp are not available because of the requirement of multiple input parameters.



### Background

For background on the development and implementation of ENVI Image Intersection see [here](http://www.harrisgeospatial.com/docs/ENVIImageIntersectionTask.html).


### Contact
Document Owner - [Kathleen Johnson](kathleen.johnson@digitalglobe.com)
