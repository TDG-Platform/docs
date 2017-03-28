# ENVI ISODATA Classification

The ISODATA method for unsupervised classification starts by calculating class means evenly distributed in the data space, then iteratively clusters the remaining pixels using minimum distance techniques. Each iteration recalculates means and reclassifies pixels with respect to the new means. This process continues until the percentage of pixels that change classes during an iteration is less than the change threshold or the maximum number of iterations is reached.   For details regarding the operation of ENVI Tasks on the Platform refer to [ENVI Task Runner](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) documentation.

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
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

envitask = gbdx.Task("ENVI_ISODATAClassification")
envitask.inputs.input_raster = data

workflow = gbdx.Workflow([ envitask ])

workflow.savedata(
    envitask.outputs.output_raster_uri,
    location="ISODATA/output_raster_uri" # edit location to suit account
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```

### Inputs

The following table lists all inputs for this task. For details regarding the use of all ENVI input types refer to the [ENVI Task Runner Inputs]([See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md)) documentation.

| Name                       | Required | Default |               Valid Values               | Description                              |
| -------------------------- | :------: | :-----: | :--------------------------------------: | ---------------------------------------- |
| file_types                 |  False   |  None   |                  string                  | GBDX Option. Comma separated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING |
| input_raster               |   True   |  None   |  A valid S3 URL containing image files.  | Specify a raster from which to run the task. -- Value Type: ENVIRASTER |
| input_raster_format        |  False   |  None   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the format of the image, for example: landsat-8. -- Value Type: STRING |
| input_raster_band_grouping |  False   |  None   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING |
| input_raster_filename      |  False   |  None   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING |
| change_threshold_percent   |  False   |  '2.0'  |              string double               | The change threshold percentage that determines when to complete the classification.  When the percentage of pixels that change classes during an iteration is less than the threshold value, the classification completes. -- Value Type: DOUBLE |
| number_of_classes          |  False   |   '5'   |               string uint                | The requested number of classes to generate. -- Value Type: UINT |
| iterations                 |  False   |  '10'   |               string uint                | The maximum iterations to perform.  If the change threshold percent is not met before the maximum number of iterations is reached, the classification completes. -- Value Type: UINT |
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

The following table lists all applicable runtime outputs for the QuickStart Script. (This section will be completed the Algorithm Curation team). For details on the methods of testing the runtimes of the task visit the following link: (INSERT link to GBDX U page here).

| Sensor Name | Total Pixels | Total Area (k2) | Time(secs) | Time/Area k2 |
| ----------- | :----------: | --------------- | ---------- | ------------ |
| QB          |  41,551,668  | 312.07          | 308.27     | 0.99         |
| WV02        |  35,872,942  | 329.87          | 1,939.17   | 5.88         |
| WV03        |  35,371,971  | 196.27          | 858.28     | 4.37         |
| GE          |  57,498,000  | 332.97          | 490.32     | 1.47         |



### Advanced Options

This script links the [Advanced Image Preprocessor](https://github.com/TDG-Platform/docs/blob/master/Advanced_Image_Preprocessor.md) to the ENVI ISODATA Classification task.

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
isodata.inputs.number_of_classes = '10'
isodata.inputs.iterations = '16'

workflow = gbdx.Workflow([ aoptask, isodata ])

workflow.savedata(
    envitask.outputs.output_raster_uri,
    location="ISODATA/output_raster_uri" # edit location to suit account
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```



###  Background

For background on the development and implementation of ISO Classification refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/classificationtutorial.html), or ENVI's task documentation [here](https://www.harrisgeospatial.com/docs/ENVIISODATAClassificationTask.html)

###Contact Us

Document Owner - [Kathleen Johnson](#kathleen.johnson@digitalglobe.com)
