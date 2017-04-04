# ENVI Classification Sieving

The Sieving task solves the issue of isolated single pixels in a classification . With a classification image as input, the task uses a filter of 4 to 8 pixels to determine if a pixel is isolated within a group.  The isolated pixels identified by the algorithm will then be written in a new raster as 'unclassified'. Use ENVIClassificationClumpingTask to remove the black pixels.

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
#	Note: Inpout raster must be a classification image, see advanced for example
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

envi = gbdx.Task("ENVI_ClassificationSieving")
envi.inputs.input_raster = sieve.outputs.output_raster_uri.value

workflow = gbdx.Workflow([envi])

workflow.savedata(
    envi.outputs.output_raster_uri,
    location="Sieving/output_raster_uri" # edit location to suit account
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
| minimum_size               |  False   |   '2'   |                  string                  | Specify the minimum size of a blob to keep. If a minimum size is not defined, the minimum size will be set to two. -- Value Type: UINT |
| pixel_connectivity         |  False   |   '8'   |                  string                  | Specify 4 (four-neighbor) or 8 (eight-neighbor) regions around a pixel are searched, for continuous blobs. -- Value Type: UINT |
| class_order                |  False   |  None   |                  string                  | Specify the order of class names in which sieving is applied to the classification image. If you do not specify this keyword, the classes are processed from first to last. -- Value Type: STRING[*] |
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

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team). For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here).

| Sensor Name | Total Pixels | Total Area (k2) | Time(secs) | Time/Area k2 |
| ----------- | :----------: | --------------- | ---------- | ------------ |
| QB          |  41,551,668  | 312.07          | 172.11     | 0.55         |
| WV02        |  35,872,942  | 329.87          | 175.47     | 0.53         |
| WV03        |  35,371,971  | 196.27          | 189.05     | 0.96         |
| GE          |  57,498,000  | 332.97          | 171.95     | 0.52         |



### Advanced

Workflow example AOP -> Classification -> Sieve - Clump.

```python
from gbdxtools import Interface
gbdx = Interface()

# Edit the following path to reflect a specific path to an image
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

aoptask = gbdx.Task("AOP_Strip_Processor") 
aoptask.inputs.data = data
aoptask.inputs.enable_dra = False
aoptask.inputs.bands = 'MS'

isodata = gbdx.Task("ENVI_ISODATAClassification")
isodata.inputs.input_raster = aop2task.outputs.data.value

sieve = gbdx.Task("ENVI_ClassificationSieving")
sieve.inputs.input_raster = isodata.outputs.output_raster_uri.value
sieve.inputs.pixel_connectivity = '4'

clump = gbdx.Task("ENVI_ClassificationClumping")
clump.inputs.input_raster = sieve.outputs.output_raster_uri.value

workflow = gbdx.Workflow([isodata, sieve, clump])

workflow.savedata(
    clump.outputs.output_raster_uri,
    location="SieveClump/output_raster_uri" # edit location to suit account
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```



### Background

For background on the development and implementation of Classification Sieving refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/sievingclasses.html),  and ENVI's task documentation [here](https://www.harrisgeospatial.com/docs/ENVIClassificationSievingTask.html).


### Contact Us
Document Owner - [Kathleen Johnson](kajohnso@digitalglobe.com)
