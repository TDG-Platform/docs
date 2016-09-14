# ENVI_QuerySpectralIndices

### Description
This task returns a string array of the spectral indices that can be computed for a given input raster, based on its wavelength metadata.

This task can be run with Python using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/)

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and output structure.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Issues](#issues) - Current or past known issues.
 * [Runtime](#runtime) - Results of task benchmark tests.
 * [Background](#background) - Background information.
 * [Contact](#contact) - Contact information.

### Quickstart

Quick start example.

```python
# Quickstart example for ENVI_QuerySpectralIndices.
from gbdxtools import Interface
gbdx = Interface()

aop2envi = gbdx.Task("AOP_ENVI_HDR")
aop2envi.inputs.image = 's3://gbd-customer-data/path_to_image'

envi_query = gbdx.Task("ENVI_QuerySpectralIndices")
envi_query.inputs.input_raster = aop2envi.outputs.output_data.value
envi_query.inputs.file_types = "hdr"

workflow = gbdx.Workflow([aop2envi, envi_query])

workflow.savedata(
  envi_query.outputs.task_meta_data,
    location='ENVI_QuerySpectralIndices'
)

workflow.execute()
status = workflow.status["state"]
wf_id = workflow.id
```

### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
file_types|False|None| .hdr, .tif |GBDX Option. Comma separated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING
input_raster|True|None| |Specify a raster to query for available spectral indices. -- Value Type: ENVIRASTER

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
task_meta_data|True|None|s3 location |GBDX Option. Output location for task meta data such as execution log and output JSON
available_indices|false|None| NA |A string array with the spectral indices that can be computed for the input raster. -- Value Type: STRING

**Output structure**

The output of this task is a Json file listing the available indices, based on the bands available in the image file. Alternatively, the output of this task can be used as input for the ENVI Spectral Indices task.  Based on the available_indices output from this task, it is possible specify the list as input for the Spectral Indices task.


### Advanced
```Python

from gbdxtools import Interface
gbdx = Interface()

data = "s3://receiving-dgcs-tdgplatform-com/pathto_1B_image"
aoptask = gbdx.Task('AOP_Strip_Processor', data=data, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)    
# creates acomp'd multispectral image

aop2envi = gbdx.Task("AOP_ENVI_HDR")
aop2envi.inputs.image = aoptask.outputs.data.value


envi_query = gbdx.Task("ENVI_QuerySpectralIndices")
envi_query.inputs.input_raster = aop2envi.outputs.output_data.value
envi_query.inputs.file_types = "hdr"


workflow = gbdx.Workflow([aoptask, aop2envi, envi_query])

workflow.savedata(
  envi_query.outputs.task_meta_data,
    location='Auto-docs/ENVI/Query'
)

workflow.execute()
status = workflow.status["state"]
wf_id = workflow.id

```

### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Average runtime  |  Total Area (k2)  |  Time(sec)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB | 41,551,668 | 312.07 | 158.26 | 0.51 |
WV01| 1,028,100,320 |351.72 | NA|NA |
WV02|35,872,942|329.87|176.04 | 0.53|
WV03|35,371,971|196.27| 232.00|1.18 |
GE| 57,498,000|332.97|241.53 | 0.73|

### Issues
Additional parsing of the output list of indices is necessary before using the list as input for the ENVI Spectral Indices task. An example of this workflow is in development.  

### Background
For background on the development and implementation of ENVI Query Spectral Indices see [here](http://www.harrisgeospatial.com/docs/ENVIQuerySpectralIndicesTask.html).


### Contact
Document Owner - Carl Reeder - creeder@digitalglobe.com
