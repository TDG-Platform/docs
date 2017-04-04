# ENVI_ClassificationToShapefile

### Description
The task exports one or more classes to a single shapefile. The vectors include separate records for each polygon.

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
#	Note: Input raster must be a classification image, see advanced for example
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

envi = gbdx.Task("ENVI_ClassificationToShapefile")
envi.inputs.input_raster = data

workflow = gbdx.Workflow([ envi ])

workflow.savedata(
  envi.outputs.output_vector_uri,
    location="Class2Shape/output_vector_uri" # edit location to suit account
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
| export_class_clrs          |  False   |  True   |                True/False                | Set this property to export CLASS_CLRS (class colors) as a shapefile attribute for each polygon. The options are true (default) or false. -- Value Type: BOOL |
| export_classes             |  False   |  None   |          array of string names           | Specify a string array with class names to export to the shapefile. To edit names of the classes you may manually edit the names in the .hdr output, or use a software package to edit the attribute names. -- Value Type: STRING[*] |
| export_area                |  False   |  True   |                True/False                | Set this property to export AREA as a shapefile attribute for each polygon. The options are true (default) or false. -- Value Type: BOOL |
| output_vector_uri_filename |  False   |  None   |                  string                  | Specify a string with the fully-qualified path and filename for OUTPUT_VECTOR. -- Value Type: STRING |



### Outputs

The following table lists all the tasks outputs.

| Name              | Required | Description                              |
| ----------------- | :------: | ---------------------------------------- |
| output_vector_uri |   True   | Output for OUTPUT_VECTOR.                |
| task_meta_data    |  False   | GBDX Option. Output location for task meta data such as execution log and output JSON. |

##### Output Structure

The output_vector shape file will be written to the specified S3 Customer Account Location in standard .shp format with supporting files. 



### Runtime

The following table lists runtime outputs for applicable sensors. For details on the methods of testing the runtimes of the task visit the following link: (INSERT link to GBDX U page here)

| Sensor Name | Total Pixels | Total Area (k2) | Time(secs) | Time/Area k2 |
| ----------- | :----------: | --------------- | ---------- | ------------ |
| QB          |  41,551,668  | 312.07          | 1,337.20   | 4.28         |
| WV02        |  35,872,942  | 329.87          | 1,806.83   | 5.48         |
| WV03        |  35,371,971  | 196.27          | 18,209.79  | 92.78        |
| GE          |  57,498,000  | 332.97          | 3,012.48   | 9.05         |



### Advanced
Include example(s) with complicated parameter settings and/or example(s) where the task is used as part of a workflow involving other GBDX tasks.

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
isodata.inputs.input_raster = aop.outputs.data.value

shp = gbdx.Task("ENVI_ClassificationToShapefile")
shp.inputs.input_raster = isodata.outputs.output_raster_uri.value
shp.inputs.export_class_clrs = False
shp.inputs.export_area = False

workflow = gbdx.Workflow([aoptask, isodata, shp])

workflow.savedata(
  shp.outputs.output_vector_uri,
    location="Class2Shape/output_vector_uri" # edit location to suit account
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```



### Background
For background on the development and implementation of this task see [here](http://www.harrisgeospatial.com/docs/ENVIClassificationToShapefileTask.html).



### Contact

Document Owner - [Kathleen Johnson](#kathleen.johnson@digitalglobe.com)
