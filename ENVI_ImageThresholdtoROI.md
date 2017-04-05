# ENVI Image Threshold To ROI

This task creates ROIs from band thresholds. You can specify one or more thresholds for one or more ROIs.

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

envi = gbdx.Task("ENVI_ImageThresholdToROI")
envi.inputs.input_raster = data
envi.inputs.roi_name = '["Water", "Land"]'
envi.inputs.roi_color = '[[0,255,0],[0,0,255]]'
envi.inputs.threshold = '[[138,221,0],[222,306,0]]'
envi.inputs.output_roi_uri_filename = "roi"

workflow = gbdx.Workflow([envi])

workflow.savedata(
    envi.outputs.output_roi_uri,
    location='ImgThreshToROI/output_roi_uri'
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```
### Inputs

The following table lists all inputs for this task. For details regarding the use of all ENVI input types refer to the [ENVI Task Runner Inputs]([See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md)) documentation.**

| Name                       | Required | Default |               Valid Values               | Description                              |
| -------------------------- | :------: | :-----: | :--------------------------------------: | ---------------------------------------- |
| input_raster               |   True   |  None   |  A valid S3 URL containing image files.  | Specify a raster from which to run the task. -- Value Type: ENVIRASTER |
| input_raster_format        |  False   |  None   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the format of the image, for example: landsat-8. -- Value Type: STRING |
| input_raster_band_grouping |  False   |  None   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING |
| input_raster_filename      |  False   |  None   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING |
| roi_color                  |   True   |  None   |            string byte array             | Specify a (3,n) byte array with the RGB colors for each ROI, where n is the number of ROIs specified by ROI_NAME. -- Value Type: BYTE[3, *] |
| threshold                  |   True   |  None   |           string double array            | specify an array that represents a threshold: [minimum, maximum, zero-based band number] You can have one or more thresholds to one or more ROIs.  -- Value Type: DOUBLE[3, *] |
| roi_name                   |   True   |  None   |               string array               | Specify a string or array of strings with the names of each ROI. -- Value Type: STRING[*] |
| output_roi_uri_filename    |  False   |  None   |                  string                  | Specify a string with the fully-qualified path and filename for OUTPUT_ROI. -- Value Type: STRING |



### Outputs

The following table lists all the tasks outputs.

| Name           | Required | Description                              |
| -------------- | :------: | ---------------------------------------- |
| output_roi_uri |   True   | Output for OUTPUT_ROI.                   |
| task_meta_data |  False   | GBDX Option. Output location for task meta data such as execution log and output JSON. |

##### Output Structure

The output_roi file(s) will be written in .xml format.



### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team). For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here).

| Sensor Name | Total Pixels | Total Area (k2) | Time(secs) | Time/Area k2 |
| ----------- | :----------: | --------------- | ---------- | ------------ |
| QB          |  41,551,668  | 312.07          | 158.62     | 0.51         |
| WV02        |  35,872,942  | 329.87          | 167.47     | 0.51         |
| WV03        |  35,371,971  | 175.47          | 0.89       | .89          |
| GE          |  57,498,000  | 162.43          | 0.49       | 0.49         |



### Advanced

To link the workflow of 1 input image into AOP_Strip_Processor and the Image Threshold to ROI task, use the following GBDX tools script in python.

```python
from gbdxtools import Interface
gbdx = Interface()

# Edit the following path to reflect a specific path to an image
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

aoptask = gbdx.Task("AOP_Strip_Processor") 
aoptask.inputs.data = data
aoptask.inputs.enable_dra = False
aoptask.inputs.bands = 'MS'

# Capture AOP task outputs
#orthoed_output = aoptask.get_output('data')

task = gbdx.Task("ENVI_ImageThresholdToROI")
task.inputs.input_raster = aoptask.outputs.data.value
task.inputs.roi_name = '["Water", "Land"]'
task.inputs.roi_color = '[[0,255,0],[0,0,255]]'
task.inputs.threshold = '[[138,221,0],[222,306,0]]'
task.inputs.output_roi_uri_filename = "roi"

workflow = gbdx.Workflow([ aoptask, task ])

workflow.savedata(
    task.outputs.output_roi_uri,
    location='ImgThreshToROI/output_roi_uri'
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```



### Background


For background on the development and implementation of Spectral Index refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/enviimagethresholdtoroitask.html).

###Contact Us
Document Owner - [Kathleen Johnson](#kathleen.johnson@digitalglobe.com)
