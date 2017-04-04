# ENVI Classification Clumping

This task performs a clumping method on a classification image. This operation clumps adjacent similar classified areas using morphological operators. Classified images often suffer from a lack of spatial coherency (speckle or holes in classified areas). Low pass filtering could be used to smooth these images, but the class information would be contaminated by adjacent class codes. Clumping classes solves this problem. The selected classes are clumped together by first performing a dilate operation then an erode operation on the classified image using one specified kernel (structuring element) for each operation

This task requires a classification has been run as in the example workflow below. 



### Table of Contents

- [Quickstart](#quickstart) - Get started!
- [Inputs](#inputs) - Required and optional task inputs.
- [Outputs](#outputs) - Task outputs and example contents.
- [Runtime](#runtime) - Example estimate of task runtime.
- [Advanced](#advanced) - Additional information for advanced users.
- [Contact Us](#contact-us) - Contact tech or document owner.](#contact-us)



### Quickstart

Example Script: Run in a python environment (i.e. - IPython) using the gbdxtools interface.

```python
from gbdxtools import Interface
gbdx = Interface()

# Edit the following path to reflect a specific path to an image
#	Note: Inpout raster must be a classification image, see advanced for example
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

envi = gbdx.Task("ENVI_ClassificationClumping")
envi.inputs.input_raster = sieve.outputs.output_raster_uri.value

workflow = gbdx.Workflow([envi])

workflow.savedata(
    envi.outputs.output_raster_uri,
    location="Clumping/output_raster_uri" # edit location to suit account
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```

### Inputs

The following table lists all inputs for this task. For details regarding the use of all ENVI input types refer to the [ENVI Task Runner Inputs]([See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md)) documentation.

| Name                       | Required |               Default               |               Valid Values               | Description                              |
| -------------------------- | :------: | :---------------------------------: | :--------------------------------------: | ---------------------------------------- |
| input_raster               |   True   |                None                 |  A valid S3 URL containing image files.  | Specify a raster from which to run the task. -- Value Type: ENVIRASTER |
| input_raster_format        |  False   |                None                 | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the format of the image, for example: landsat-8. -- Value Type: STRING |
| input_raster_band_grouping |  False   |                None                 | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING |
| input_raster_filename      |  False   |                None                 | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING |
| dilate_kernel              |   True   | '[[1, 1, 1], [1, 1, 1], [1, 1, 1]]' |            string uint array             | Specify 2D array of zeros and ones that represents the structuring element (kernel) used for a dilate operation.Dilation is a morphological operation that uses a structuring element to expand the shapes contained in the input image. -- Value Type: UINT[*, *] |
| erode_kernel               |   True   | '[[1, 1, 1], [1, 1, 1], [1, 1, 1]]' |                  string                  | Specify 2D array of zeros and ones that represents the structuring element (kernel) used for an erode operation. -- Value Type: UINT[*, *] |
| class_order                |  False   |        [first to last order]        |                  string                  | Specify the order of class names in which sieving is applied to the classification image. -- Value Type: STRING[*] |
| output_raster_uri_filename |  False   |                None                 |                  string                  | Specify a string with the fully-qualified path and filename for OUTPUT_RASTER. -- Value Type: STRING |

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
| QB          |  41,551,668  | 312.07          | 155.93     | 0.5          |
| WV02        |  35,872,942  | 329.87          | 171.72     | 0.52         |
| WV03        |  35,371,971  | 196.27          | 173.03     | 0.88         |
| GE          |  57,498,000  | 332.97          | 173.03     | 0.52         |



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

clump = gbdx.Task("ENVI_ClassificationClumping")
clump.inputs.input_raster = sieve.outputs.output_raster_uri.value
clump.inputs.dilate_kernel = '[[1,0,1] [1,0,1] [1,0,1]]'

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

For background on the development and implementation of Classification Clumping refer to the [ENVI Documentation](http://www.harrisgeospatial.com/docs/enviclassificationclumpingtask.html)

###Contact Us

Document Owner - [Kathleen Johnson](#kathleen.johnson@digitalglobe.com)
