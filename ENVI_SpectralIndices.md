# ENVI_SpectralIndices

### Description
This task creates a spectral index raster with one or more bands, where each band represents a different spectral index. Spectral indices are combinations of surface reflectance at two or more wavelengths that indicate relative abundance of features of interest.

This task can be run with Python using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/)

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and output structure.
 * [Advanced](#advanced) - Additional information for advanced users.
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
aop2envi.inputs.image = 's3://gbd-customer-data/PathToDeliveredImage'
envi_ndvi = gbdx.Task("ENVI_SpectralIndices")
envi_ndvi.inputs.input_raster = aop2envi.outputs.output_data.value
envi_ndvi.inputs.file_types = "hdr"
# Specify a string/list of indicies to run on the input_raster variable.  The order of indicies wi
envi_ndvi.inputs.index = '["Normalized Difference Vegetation Index", "WorldView Soil Index"]'
workflow = gbdx.Workflow([aop2envi, envi_ndvi])
workflow.savedata(
	       aop2envi.outputs.output_data,
	          location='Auto-docs/ENVI/SIS'
)
workflow.savedata(
	       envi_ndvi.outputs.output_raster_uri,
	          location='Auto-docs/ENVI/SIS'
)
workflow.execute()
status = workflow.status["state"]
wf_id = workflow.id
# print wf_id
# print status
```

### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
file_types|False|None| |GBDX Option. Comma seperated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING[*]
index|True|None| |Specify a string, or array of strings, representing the pre-defined spectral indices to apply to the input raster. -- Value Type: STRING[*]
input_raster|True|None|.TIF .HDR |Specify a raster from which to generate a spectral index raster. -- Value Type: ENVIRASTER
output_raster_uri_filename|False|None| string |Outputor OUTPUT_RASTER. -- Value Type: ENVIURI

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


### Issues
Currently the task in the Web App 2.0 will process an image with NDVI and the WorldView soil index listed in the quickstart example (Aug 8th, 2016). However, custom workflows with gbdxtools may include any of the indices compatible with the task (see link in Advanced section)

### Background

For background on the development and implementation of Spectral Index refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/spectralindices.html)


### Contact
Document Owner - Carl Reeder - creeder@digitalglobe.com
