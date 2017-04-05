
# ENVI ROI To Classification

This task creates a classification image from regions of interest (ROIs).  The input ROI file must be created using the [ENVI_ImageThresholdToROI Task](https://github.com/TDG-Platform/docs/blob/master/ENVI_ImageThresholdtoROI.md).  You may use a pre-existing ROI dataset or  produce the final classification as part of a larger workflow. Examples are included in the Advanced Options.  For the best result, the thresholds may need to be manually adjusted. For details regarding the operation of ENVI Tasks on the Platform refer to [ENVI Task Runner](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md).

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
input_raster_data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'
input_roi_data = 's3://gbd-customer-data/CustomerAccount#/PathToROIFile/'

classtask = gbdx.Task("ENVI_ROIToClassification")
classtask.inputs.input_raster = input_raster_data
classtask.inputs.input_roi = input_roi_data

workflow = gbdx.Workflow([ classtask ])

workflow.savedata(
    classtask.outputs.output_raster_uri, 
    location='ROIToClassification/output_raster_uri' # edit location to suit account
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
| input_roi                  |   True   |   N/A   |              A valid S3 URL              | Specify an ROI or array of ROIs used to create the classification image. -- Value Type: [ENVIROI](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md#enviroi)[*] |
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

The following table lists all applicable runtime outputs for the ENVI ROI to Classification. An estimated Runtime for the Advanced Script example can be derived from adding the result for the two pre-processing steps.

| Sensor Name | Total Pixels | Total Area (k2) | Time(secs) | Time/Area k2 |
| ----------- | :----------: | --------------- | ---------- | ------------ |
| QB02        |  41,551,668  | 312.07          | 172.56     | 0.55         |
| WV02        |  35,872,942  | 329.87          | 173.40     | 0.53         |
| WV03        |  35,371,971  | 196.27          | 197.48     | 0.88         |
| GE01        |  57,498,000  | 332.97          | 184.30     | 0.55         |



### Advanced

To link the workflow of 1 input image into AOP_Strip_Processor and into the ENVI ROI To CLassification task you must use the following GBDX tools script python example:

```python
from gbdxtools import Interface
gbdx = Interface()

# Edit the following path to reflect a specific path to an image
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

aoptask = gbdx.Task("AOP_Strip_Processor") 
aoptask.inputs.data = data
aoptask.inputs.enable_dra = False
aoptask.inputs.bands = 'MS'

threshold = gbdx.Task("ENVI_ImageThresholdToROI")
threshold.inputs.input_raster = aoptask.outputs.data.value
threshold.inputs.roi_name = "[\"Water\", \"Land\"]"
threshold.inputs.roi_color = "[[0,255,0],[0,0,255]]"
threshold.inputs.threshold = "[[138,221,0],[222,306,0]]"
threshold.inputs.output_roi_uri_filename = "roi"

roitoclass = gbdx.Task("ENVI_ROIToClassification")
roitoclass.inputs.input_raster = aoptask.outputs.data.value
roitoclass.inputs.input_roi = threshold.outputs.output_roi_uri.value

workflow = gbdx.Workflow([ aoptask, threshold, roitoclass ])

workflow.savedata(
    roitoclass.outputs.output_raster_uri,
    location='ROIToClassification/output_raster_uri'
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```



### Background

For background on the development and implementation of ROI to Classification refer to the [ENVI Documentation](http://www.harrisgeospatial.com/docs/enviroitoclassificationtask.html).




### Contact Us
Document Owner - [Kathleen Johnson](kajohnso@digitalglobe.com)
