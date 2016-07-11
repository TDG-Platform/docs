# ENVI_Spectral_Index

ENVI_Spectral_Index. This task creates a spectral index raster from one pre-defined spectral index. Spectral indices are combinations of surface reflectance at two or more wavelengths that indicate relative abundance of features of interest. This task is used to compute a single index on a combination of multi spectral bands within an image. This task can be used to compute indices such as the Normalized Difference Vegetation Index (NDVI). An index such as NDVI will be passed into the task and a single band raster with the results of the index will be returned as output.
Note:  The wavelength metadata is not available in the correct format from the AOP task. Therefore this task is dependent on the "AOP_ENVI_HDR" task  

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Known Issues](#known-issues) - current or past issues known to exist.

### Quickstart

This script gives the example of ENVI Spectral Index with a single tif file as input. 

```python
# Quickstart **Example Script Run in Python using the gbdxTools InterfaceExample producing a single band vegetation mask from a tif file.
# First Initialize the Environment
	
    from gbdxtools import Interface
    gbdx = Interface()
    
    aop2envi = gbdx.Task("AOP_ENVI_HDR")
    aop2envi.inputs.image = 's3://gbd-customer-data/a157fdce-bb1d-42b3-96a9-66942896a787/denver_aop'
    
	envi_ndvi = gbdx.Task("ENVI_SpectralIndex")
    envi_ndvi.inputs.input_raster = aop2envi.outputs.output_data.value
    envi_ndvi.inputs.file_types = "hdr"
    envi_ndvi.inputs.index = "Normalized Difference Vegetation Index"

    workflow = gbdx.Workflow([aop2envi, envi_ndvi])
    workflow.savedata(
       aop2envi.outputs.output_data,
       location='NDVI/output_data'
    )
    workflow.savedata(
       envi_ndvi.outputs.output_raster_uri,
       location='NDVI/output_raster_uri'
    )

    print workflow.execute()
```
	
### Inputs	
**Description of Input Parameters and Options for the "ENVI_Spectral_Index":**
This task will work on Digital Globe images with a IMD file located in the S3 location: 
Input imagery sensor types include: QuickBird, WorldView 1, WorldView 2, WorldView 3 and GeoEye
The following table lists the Spectral Index task inputs.
All inputs are **required**

Name                     |       Default         |        Valid Values             |   Description
-------------------------|:---------------------:|---------------------------------|-----------------
raster                   |          N/A          | S3 URL   .TIF only              | S3 location of input .tif file processed through AOP_Strip_Processor.
data                     |         true          | Folder name in S3 location      | This will explain the output file location and provide the output in .TIF format.

**OPTIONAL SETTINGS: Required = False**

* NA - No additional optional settings for this task exist


### Outputs

The following table lists the Spectral Index task outputs.

Name | Required |   Description
-----|:--------:|-----------------
data |     Y    | This will explain the output file location and provide the output in .TIF format.
log  |     N    | S3 location where logs are stored.


**Description of Output and options for the "ENVI_Spectral_Index":**
This task will provide a raster of the spectral index output in both an ENVI hdr format and tif format. 

**Data Structure for Expected Outputs:**

The processed imagery will be written to the specified S3 Customer Location in a 1 band TIF format(e.g.  s3://gbd-customer-data/unique customer id/named directory/). 

### Advanced
To link the workflow of 1 input image into AOP_Strip_Processor into a protogen task you must use the follow GBDX tools script in python

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

 

###Known Issues
1) To run the task in a single workflow with AOP the tif file must first be removed from the AOP folder with the additional python commands listed in Advanced


For background on the development and implementation of Spectral Index refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/spectralindices.html)

