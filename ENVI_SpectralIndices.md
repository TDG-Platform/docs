# ENVI_SpectralIndices

### Description
This task creates a spectral index raster with one or more bands, where each band represents a different spectral index. Spectral indices are combinations of surface reflectance at two or more wavelengths that indicate relative abundance of features of interest.

This task can be run with Python using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/)

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and output structure.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Runtime](#runtime) - Example estimate of task runtime.
 * [Issues](#issues) - Current or past known issues.
 * [Background](#background) - Background information.
 * [Contact](#contact) - Contact information.

### Quickstart
Quick start example.

```python

# Quickstart **Example Script Run in Python using the gbdxTools InterfaceExample producing a single band vegetation mask from a tif file.
# First Initialize the Environment
from gbdxtools import Interface
gbdx = Interface()

aop2envi = gbdx.Task("AOP_ENVI_HDR")
#Edit the following path to reflect a specific path to an image
aop2envi.inputs.image = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'
envi_ndvi = gbdx.Task("ENVI_SpectralIndices")
envi_ndvi.inputs.input_raster = aop2envi.outputs.output_data.value
envi_ndvi.inputs.file_types = "hdr"
# Specify a string/list of indicies to run on the input_raster variable.  The order of indicies wi
envi_ndvi.inputs.index = '["Normalized Difference Vegetation Index", "WorldView Soil Index"]'

#Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
workflow = gbdx.Workflow([aop2envi, envi_ndvi])
workflow.savedata(
	       aop2envi.outputs.output_data,
	          location='ENVI/spectralindices'
)
workflow.savedata(
	       envi_ndvi.outputs.output_raster_uri,
	          location='ENVI/spectralindices'
)
workflow.execute()
status = workflow.status["state"]
wf_id = workflow.id
# print wf_id
# print status
```

### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False). For details regarding the use of input ports refer to the [ENVI Task Runner](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner.md) documentation.

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
input_raster             |          N/A          | S3 URL   .TIF and .hdr only     | S3 location of input .tif file processed through AOP_Strip_Processor.
index                    |          N/A          |     string of index name        | Specify a string, or array of strings, representing the pre-defined spectral indices to apply to the input raster.
input_raster_band_grouping| N/A                  | Sensor Specific [See input port documentation](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner.md#ENVIRPCRasterSpatialRef) | Specify band group e.g. "multispectral".  input_raster_band_grouping "panchromatic" will not function in the Spectral Index task.
output_raster_uri_filename | N/A | string name for output e.g. "NDVI" | output raster file name 
### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
task_meta_data|False|None|.log |GBDX Option. Output location for task meta data such as execution log and output JSON
output_raster_uri|True|None|.TIF |Outputor OUTPUT_RASTER. -- Value Type: ENVIURI

**Output structure**

The output of this task will be a single tif with multiple bands representing the indices listed.


### Advanced
For advanced parameters and a full list of indices compatible with this task refer to the following link:
http://www.harrisgeospatial.com/docs/alphabeticallistspectralindices.html

Example of workflow with Spectral Indices including preprocessing steps in gbdxtools

```python

from gbdxtools import Interface
gbdx = Interface()

#Edit the following path to reflect a specific path to an image
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'
aoptask = gbdx.Task('AOP_Strip_Processor', data=data, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image

aop2envi = gbdx.Task("AOP_ENVI_HDR")
aop2envi.inputs.image = aoptask.outputs.data.value

envi_ndvi = gbdx.Task("ENVI_SpectralIndices")
envi_ndvi.inputs.input_raster = aop2envi.outputs.output_data.value
envi_ndvi.inputs.file_types = "hdr"
# Specify a string/list of indicies to run on the input_raster variable.  The order of indicies wi
envi_ndvi.inputs.index = '["Normalized Difference Vegetation Index", "WorldView Built-Up Index", "WorldView Non-Homogeneous Feature Difference", "WorldView Water Index", "WorldView Soil Index"]'

workflow = gbdx.Workflow([aoptask, aop2envi, envi_ndvi])
#Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
workflow.savedata(
   aop2envi.outputs.output_data,
      location='ENVI/SpectralIndices/AOP'
)

workflow.savedata(
   envi_ndvi.outputs.output_raster_uri,
      location='ENVI/SpectralIndices'
)

workflow.execute()
workflow.status
```

### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  | Total Pixels |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB | 41,551,668 | 312.07 | 184.23 | 0.59
WV01| 1,028,100,320 |351.72 | NA| NA
WV02|35,872,942|329.87| 215.81|0.65
WV03|35,371,971|196.27| 247.30|1.26
GE| 57,498,000|332.97|216.80 |0.65


### Issues
Currently the advanced task in the Web App 2.0 will process an image with Normalized Difference Vegetation Index, WorldView Built-Up Index, WorldView Non-Homogeneous Feature Difference, WorldView Water Index, WorldView Soil Index (Aug 8th, 2016). However, custom workflows with gbdxtools may include any of the indices compatible with the task (see link in Advanced section)

### Background

For background on the development and implementation of Spectral Index refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/spectralindices.html)


### Contact
Document Owner - Carl Reeder - creeder@digitalglobe.com
