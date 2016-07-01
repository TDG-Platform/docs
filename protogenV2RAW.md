# 8-Band water Mask (protogenV2RAW)

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Known Issues](#known-issues) - Current or past issues known to exist.

### Quickstart
This script gives the example of RAW with a single tif file as input. 

```python
# Quickstart Example producing a single band vegetation mask from a tif file.
# First Initialize the Environment
	
	from gbdxtools import Interface 
    import json
    gbdx = Interface()
    raster = 's3://gbd-customer-data/PathToImage/image.tif'
    prototask = gbdx.Task("protogenV2RAW", raster=raster)

    workflow = gbdx.Workflow([ prototask ])  
    workflow.savedata(prototask.outputs.data, location="RAW")
    workflow.execute()

    print workflow.id
    print workflow.status
```	
### Inputs

This task will process only WorldView 2 or WorldView 3 multi-spectral imagery (8-band optical and VNIR data sets) that has been atmospherically compensated by the AOP processor.  Supported formats are .TIF, .TIL, .VRT, .HDR.

The following table lists the RAW Protogen task inputs.
All inputs are **required**

Name                     |       Default         |        Valid Values             |   Description
-------------------------|:---------------------:|---------------------------------|-----------------
raster                   |          N/A          | S3 URL   .TIF only              | S3 location of input .tif file processed through AOP_Strip_Processor.
data                     |         true          | Folder name in S3 location      | This will explain the output file location and provide the output in .TIF format.

**OPTIONAL SETTINGS: Required = False**

* NA - No additional optional settings for this task exist


### Outputs

The following table lists the RAW Protogen task outputs.

Name | Required |   Description
-----|:--------:|-----------------
data |     Y    | This will explain the output file location and provide the output in .TIF format.
log  |     N    | S3 location where logs are stored.


### Advanced
To link the workflow of 1 input image into AOP_Strip_Processor into a protogen task you must use the follow GBDX tools script in python

```python
#First initalize the environment 
#AOP strip processor has input values known to complete the Protogen tasks

from gbdxtools import Interface
gbdx = Interface()

data = "s3://receiving-dgcs-tdgplatform-com/055026839010_01_003"

aoptask2 = gbdx.Task('AOP_Strip_Processor', data=data, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image

gluetask = gbdx.Task('gdal-cli')      # move aoptask output to root where prototask can find it
gluetask.inputs.data = aoptask2.outputs.data.value
gluetask.inputs.execution_strategy = 'runonce'
gluetask.inputs.command = """mv $indir/*/*.tif $outdir/"""
prototask = gbdx.Task('protogenV2RAW')
prototask.inputs.raster = gluetask.outputs.data.value


workflow = gbdx.Workflow([aoptask2, gluetask, prototask])
workflow.savedata(prototask.outputs.data, 'RAW')
  
workflow.execute()

workflow.status
```

###Postman status @ 06/07/16

**Successful run with Tif file.  


**Data Structure for Expected Outputs:**

Your Processed Imagery will be written as Binary .TIF image type UINT8x1 and placed in the specified S3 Customer Location (e.g.  s3://gbd-customer-data/unique customer id/named directory/).  

###Known Issues
1) To run the task in a single workflow with AOP the tif file must first be removed from the AOP folder with the additional python commands listed in Advanced

2)False positives maybe present due to certain types of concrete roofs or shadows.

3) Testing additional input formats still in progress.  .VRT is currently not functioning (6/30/2016)**


For background on the development and implementation of  Protogen  [Documentation under development](Insert link here)

