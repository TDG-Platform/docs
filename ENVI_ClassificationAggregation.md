
# ENVI Classification Aggregation

This task aggregates smaller class regions to a larger, adjacent region as part of the classification cleanup.
For details regarding the operation of ENVI Tasks on the Platform refer to [ENVI Task Runner](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) documentation.

### Table of Contents
* [Quickstart](#quickstart) - Get started!
* [Inputs](#inputs) - Required and optional task inputs.
* [Outputs](#outputs) - Task outputs and example contents.
* [Advanced](#advanced) - Script performing multiple tasks in one workflow
* [Runtime](#runtime) - Detailed Description of Inputs
* [Contact Us](#contact-us)

### Quickstart

This task assumes that the image has been pre-processed, such as orthorectification and atmospherical correction. It is strongly recommended that the image be pre-processed using the [Advanced Image Preprocessor](https://github.com/TDG-Platform/docs/blob/master/AOP_Strip_Processor.md) (see the advanced section for an example). This task is meant to be used on an already classified image. In the example workflow below, the  [ISODATA Classification](https://github.com/TDG-Platform/docs/blob/master/ENVI_ISODATAClassification.md) task was utilized to perform the classification step on preprocessed data.

```python
from gbdxtools import Interface
gbdx = Interface()

isodata = gbdx.Task("ENVI_ISODATAClassification")
# Edit the following path to reflect a specific path to an image
isodata.inputs.input_raster = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

aggreg = gbdx.Task("ENVI_ClassificationAggregation")
aggreg.inputs.input_raster = isodata.outputs.output_raster_uri.value

workflow = gbdx.Workflow([isodata, aggreg])

workflow.savedata(
    isodata.outputs.output_raster_uri, 
    location="ClassificationAggregation/isodata"
)
workflow.savedata(
    aggreg.outputs.output_raster_uri, 
    location="ClassificationAggregation/agg"
)

print workflow.execute()

# To monitor workflow, use the following command while 
#  the Python interpreter is still open.
print workflow.status
```


### Inputs
The following table lists all inputs for this task.
Mandatory (optional) settings are listed as Required = True (Required = False).  

| Name                       | Required | Default | Valid Values                             | Description                              |
| -------------------------- | :------: | :-----: | :--------------------------------------- | ---------------------------------------- |
| file_types                 |  False   |  None   | .hdr,.tif                                | GBDX Option. Comma separated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING |
| input_raster               |   True   |  None   | A valid S3 folder containing image files. | Specify a classification raster on which to perform aggregation. |
| input_raster_format        |  False   |  None   | [More on ENVIRASTER input port](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md#enviraster) | Provide the format of the image, for example: landsat-8. -- Value Type: STRING |
| input_raster_band_grouping |  False   |  None   | [More on ENVIRASTER input port](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md#enviraster) | Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING |
| input_raster_filename      |  False   |  None   | [More on ENVIRASTER input port](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md#enviraster) | Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING |
| minimum_size               |  False   |    9    | any odd number >= 9                      | Specify the Aggregate Minimum Size in pixels. Regions with a size of this value or smaller are aggregated to an adjacent, larger region. -- Value Type: UINT |
| output_raster_uri_filename |  False   |  data*  |                                          | Specify a string with the fully-qualified path and filename for OUTPUT_RASTER. -- Value Type: STRING |

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

| Name              | Required | Valid Values | Description                              |
| ----------------- | :------: | :----------- | ---------------------------------------- |
| task_meta_data    |  False   | None         | GBDX Option. Output location for task meta data such as execution log and output JSON |
| output_raster_uri |   True   | .hdr, .tif   | Specify a string with the fully qualified filename and path of the output raster. If you do not specify this property, the output raster is only temporary. Once the raster has no remaining references, ENVI deletes the temporary file. |

**Output Structure**

Your smoothed classification file will be written to the specified S3 Customer Location in the ENVI file format and tif format(e.g.  s3://gbd-customer-data/unique customer id/named directory/classification.hdr).  

### Advanced

Included below is a complete end-to-end workflow for Advanced Image Preprocessing => ISODATA Classification => Classification Aggregation:

```python
from gbdxtools import Interface
gbdx = Interface()

# Edit the following path to reflect a specific path to an image
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'
aoptask = gbdx.Task(
    "AOP_Strip_Processor", 
    data=data, 
    enable_acomp=True, 
    bands='MS', 
    enable_pansharpen=False, 
    enable_dra=False
)

# Create ISODATA
isodata = gbdx.Task("ENVI_ISODATAClassification")
isodata.inputs.input_raster = aoptask.outputs.data.value

# Create Classification Aggregation
aggreg = gbdx.Task("ENVI_ClassificationAggregation")
aggreg.inputs.input_raster = isodata.outputs.output_raster_uri.value

# Run Workflow and Send output to  s3 Bucket
workflow = gbdx.Workflow([ aoptask, isodata, aggreg ])

# The data input and output lines must be edited to point to an authorized customer S3 location)
workflow.savedata(
    aoptask.outputs.data,
    location="ClassificationAggregation/Advanced/aop"
)

workflow.savedata(
    isodata.outputs.output_raster_uri,
    location="ClassificationAggregation/Advanced/isodata"
)

workflow.savedata(
    aggreg.outputs.output_raster_uri,
    location="ClassificationAggregation/Advanced/agg"
)

print workflow.execute()

# To monitor workflow, use the following command while 
#  the Python interpreter is still open.
print workflow.status
```

### Runtime

The following table lists all applicable runtime outputs for Classification Aggregation. An estimated Runtime for the Advanced Script example can be derived from adding the result for the two pre-processing steps. For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

| Sensor Name | Total Pixels | Total Area (k2) | Time(secs) | Time/Area k2 |
| ----------- | :----------: | --------------- | ---------- | ------------ |
| QB02        |  41,551,668  | 312.07          | 328.42     | 1.05         |
| WV02        |  35,872,942  | 329.87          | 414.51     | 1.26         |
| WV03        |  35,371,971  | 196.27          | 447.80     | 2.28         |
| GE01        |  57,498,000  | 332.97          | 419.17     | 1.26         |



### Background

For background on the development and implementation of Classification Aggregation refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/classificationtutorial.html)


###Contact Us
Document Owner - [Kathleen Johnson](kajohnso@digitalglobe.com)
