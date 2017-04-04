
# ENVI Classification Aggregation

This task aggregates smaller class regions to a larger, adjacent region as part of the classification cleanup.
For details regarding the operation of ENVI Tasks on the Platform refer to [ENVI Task Runner](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) documentation.

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
#  Note: Input raster must be a classification image, see advanced for example
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

envi = gbdx.Task("ENVI_ClassificationAggregation")
envi.inputs.input_raster = isodata.outputs.output_raster_uri.value

workflow = gbdx.Workflow([ envi ])

workflow.savedata(
    envi.outputs.output_raster_uri, 
    location="ClassAgg/output_raster_uri" # edit location to suit account
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
| minimum_size               |  False   |   '9'   |          string uint (odd >= 9)          | Specify the aggregate minimum size in pixels. Regions with a size of this value or smaller are aggregated to an adjacent, larger region. -- Value Type: UINT |
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

The following table lists all applicable runtime outputs for Classification Aggregation. An estimated Runtime for the Advanced Script example can be derived from adding the result for the two pre-processing steps. For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

| Sensor Name | Total Pixels | Total Area (k2) | Time(secs) | Time/Area k2 |
| ----------- | :----------: | --------------- | ---------- | ------------ |
| QB02        |  41,551,668  | 312.07          | 328.42     | 1.05         |
| WV02        |  35,872,942  | 329.87          | 414.51     | 1.26         |
| WV03        |  35,371,971  | 196.27          | 447.80     | 2.28         |
| GE01        |  57,498,000  | 332.97          | 419.17     | 1.26         |


### Advanced

Included below is a complete end-to-end workflow for Advanced Image Preprocessing => ISODATA Classification => Classification Aggregation:

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
isodata.inputs.input_raster = aoptask.outputs.data.value

aggreg = gbdx.Task("ENVI_ClassificationAggregation")
aggreg.inputs.input_raster = isodata.outputs.output_raster_uri.value
aggreg.inputs.minimum_size = '13'

workflow = gbdx.Workflow([ aoptask, isodata, aggreg ])


workflow.savedata(
    aggreg.outputs.output_raster_uri,
    location="ClassAgg/output_raster_uri" # edit location to suit account
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```



### Background

For background on the development and implementation of Classification Aggregation refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/classificationtutorial.html), or the ENVI's task documentation [here](https://www.harrisgeospatial.com/docs/ENVIClassificationAggregationTask.html)


### Contact Us
Document Owner - [Kathleen Johnson](kajohnso@digitalglobe.com)
