# ENVI Query Spectral Indices

### Description
This task returns a string array of the spectral indices that can be computed for a given input raster, based on its wavelength metadata.

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
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

envi = gbdx.Task("ENVI_QuerySpectralIndices")
envi.inputs.input_raster = aop2envi.outputs.output_data.value

workflow = gbdx.Workflow([envi])

workflow.savedata(
    envi_query.outputs.task_meta_data,
    location='QuerySpectralIndices/task_meta_data' # edit location to suit account
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



### Outputs
The following table lists all the tasks outputs.

| Name              | Required | Description                              |
| ----------------- | :------: | ---------------------------------------- |
| available_indices |   True   | A string array with the spectral indices that can be computed for the input raster. -- Value Type: STRING[*] |
| task_meta_data    |  False   | GBDX Option. Output location for task meta data such as execution log and output JSON. |



##### Output Structure

The output of this task is a string port listing the available indices, based on the bands available in the image file. This port can be used to chain to another task. Alternatively, the output is written to a JSON file in the `task_meta_data` port, where the list can be found after the Task completes.



### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team). For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here).

| Sensor Name | Total Pixels  | Total Area (k2) | Time(secs) | Time/Area k2 |
| ----------- | :-----------: | --------------- | ---------- | ------------ |
| QB          |  41,551,668   | 312.07          | 162.25     | 0.52         |
| WV01        | 1,028,100,320 | 351.72          | NA         | NA           |
| WV02        |  35,872,942   | 329.87          | 162.63     | 0.49         |
| WV03        |  35,371,971   | 196.27          | 177.24     | 0.90         |
| GE          |  57,498,000   | 332.97          | 162.21     | 0.49         |

### 

### Advanced

Workflow example for AOP to ENVI's Query Spectral Indices, then Spectral Indices.

```Python
from gbdxtools import Interface
gbdx = Interface()

# Edit the following path to reflect a specific path to an image
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

aoptask = gbdx.Task("AOP_Strip_Processor") 
aoptask.inputs.data = data
aoptask.inputs.enable_dra = False
aoptask.inputs.bands = 'MS'

envi_query = gbdx.Task("ENVI_QuerySpectralIndices")
envi_query.inputs.input_raster = aop2envi.outputs.output_data.value
envi_query.inputs.file_types = "hdr"

envi_si = gbdx.Task("ENVI_SpectralIndices")
envi_si.inputs.input_raster = envi_query.outputs.output_raster_uri.value
envi_si.inputs.index = envi_query.outputs.available_indices.value

workflow = gbdx.Workflow([aoptask, envi_query, envi_si])

workflow.savedata(
    envi_query.outputs.task_meta_data,
    location='AOP_Query_SpectralIndices/task_meta_data'
)

workflow.savedata(
    envi_si.outputs.output_raster_uri,
    location='AOP_Query_SpectralIndices/output_raster_uri'
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```



### Background
For background on the development and implementation of ENVI Query Spectral Indices see [here](http://www.harrisgeospatial.com/docs/ENVIQuerySpectralIndicesTask.html).


### Contact
Document Owner - Carl Reeder - creeder@digitalglobe.com
