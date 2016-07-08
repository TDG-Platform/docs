# AOP output to ENVI HDR (AOP_ENVI_HDR)

**AOP_ENVI_HDR** This task builds an ENVI .hdr file for each .tif file found in a folder. This task is used to pass wavelength metadata into .hdr format for use in subsequent tasks, such as "ENVI_Spatial_Index".  Currently the .hdr file will only explain wavelength metadata, but additional metadata will be added with updated versions.  

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Known Issues](#known issues) - current or past issues known to exist.
 
 ### Quickstart

This script gives the example of AOP_ENVI_HDR with a single output folder from AOP as input. 

**Example Script:** Run in IPython using the GBDXTools Interface

```python	
    from gbdxtools import Interface
    gbdx = Interface()
    
    aop2envi = gbdx.Task("AOP_ENVI_HDR")
    aop2envi.inputs.image = 's3://receiving-dgcs-tdgplatform-com/055249130010_01_003'
    
    workflow = gbdx.Workflow([aop2envi])
    workflow.savedata(
       aop2envi.outputs.output_data,
       location='aop2envi/output_data'
    )
    
    print workflow.execute()
```	

### Inputs	
**Description of Input Parameters and Options for the**** "AOP_ENVI_HDR":**

This task will function on Digital Globe images with an XML or IMD file located in the S3 location.  The input imagery may be either an AOP output folder or an order in 1B image format.
Input imagery sensor types include: QuickBird, WorldView 1, WorldView 2, WorldView 3 and GeoEye

The following table lists the AOP_ENVI_HDR task inputs:
All inputs are **required**

Name                     |       Default         |        Valid Values             |   Description
-------------------------|:---------------------:|---------------------------------|-----------------
inputs.image             |         true          | Directory name in S3 location   | This will explain the output file location and provide the output in .TIF format.

**OPTIONAL SETTINGS: Required = False**

* NA - No additional optional settings for this task exist

### Outputs

The following table lists the AOP_ENVI_HDR task outputs.

Name        | Required |   Description
------------|:--------:|-----------------
output_data |     Y    | This will explain the output file location and provide the output in .hdr format.

**Data Structure for Expected Outputs:**

Your processed imagery will be written to the specified S3 Customer Location in TIF format as well as the ENVI format (e.g. s3://gbd-customer-data/unique customer id/named directory/Image.tif).  


**REQUIRED SETTINGS AND DEFINITIONS:**

* S3 location of input data (1B data will process by TIL or a strip run through AOP will be in TIF format):
    * Required = ‘True’
    * type = ‘directory’
    * name = ‘image’
    
* Define the Task:
    * Required = ‘True’
    * envitask = gbdx.Task("AOP_ENVI_HDR")

* Define the Output Directory: (a gbd-customer-data location)
    * Required = ‘true’
    * type = ‘directory’
	* description = The original AOP image data with the ENVI .hdr file
    * name = "output_data"
	
**OPTIONAL SETTINGS: Required = False**
Currently additional options for this task are not available.  Updates to this task may provide options to add various metadata attributes to the .hdr file.  

### Advanced

To link the workflow of 1 input image into AOP_Strip_Processor into the ENVI Spectral Index task you must use the following GBDX tools script in python:

```python
#First initialize the environment 
#AOP strip processor has input values known to complete the Spectral Index task
from gbdxtools import Interface
gbdx = Interface()

data = "s3://receiving-dgcs-tdgplatform-com/ImageLocation"
aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')

# Capture AOP task outputs 
#orthoed_output = aoptask.get_output('data')

aop2envi = gbdx.Task("AOP_ENVI_HDR")
aop2envi.inputs.image = aoptask.outputs.data.value

envi_ndvi = gbdx.Task("ENVI_SpectralIndex")
envi_ndvi.inputs.input_raster = aop2envi.outputs.output_data.value
envi_ndvi.inputs.file_types = "hdr"
envi_ndvi.inputs.index = "Normalized Difference Vegetation Index"

workflow = gbdx.Workflow([aoptask, aop2envi, envi_ndvi])

workflow.savedata(
  aoptask.outputs.data,
  location='NDVI/AOP'
)
workflow.savedata(
  aop2envi.outputs.output_data,
  location='NDVI/hdr'
)
workflow.savedata(
  envi_ndvi.outputs.output_raster_uri,
  location='NDVI/SI/output_raster_uri'
)

print workflow.execute()

```
  
###Postman status @ 16:22 6/14/16
completed_time": null,
  "state": {
    "state": "complete",
    "event": "succeeded"
  },
  "submitted_time": "2016-06-15T17:09:34.572641+00:00",
 

###Known Issues
1)To run an extended workflow including the image preprocessing step with AOP_Strip_Processor use the advanced script. 
 
For background on the development and implementation of geoIO and this task, please refer to the GitHub documentation [ Digital Globe geoIO Documentation](https://github.com/digitalglobe/geoio)

