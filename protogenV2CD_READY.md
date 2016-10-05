# Image Pair Alignement processor (protogenV2CD_READY)

The image pair alignment (IPA) processor computes the intersection AOI or **iAOI** between the two input images. If the latter do not overlap geographically the IPA returns an error and the workflow is terminated. If they overlap, the IPA generates two new images, each containing its original contents extracted from within the given iAOI. If the spatial resolutions of the two images differ, the one with the highest is resampled using bilinear interpolation to match the resolution/dimensions of the one with the lowest. The resulting images are referred to as CD ready images.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Runtime](#runtime) - Results of task benchmark tests.
 * [Known Issues](#known-issues) - Current or past issues known to exist.
 * [Contact Us](#contact-us) - Contact tech or document owner.

### Quickstart
This script gives the example of CD_READY with a single tif file as input.

```python
# Quickstart Example producing a single band water mask from a tif file.
# First Initialize the Environment

from gbdxtools import Interface
gbdx = Interface()
post = 's3://gbd-customer-data/PathToImage/image1.tif'
pre  = 's3://gbd-customer-data/PathToImage/image2.tif'
prototask = gbdx.Task("protogenV2CD_READY", raster=post, slave=pre)

workflow = gbdx.Workflow([ prototask ])  
workflow.savedata(prototask.outputs.data, location="cdready/post")
workflow.savedata(prototask.outputs.slave,location="cdready/pre")
workflow.execute()

print workflow.id
print workflow.status
```
### Inputs

This task will process any pair of geocoded images that have a non void geographic intersection. Both images need to be of the same format and same number of bands. Supported formats are .TIF, .TIL, .VRT, .HDR.

The following table lists the CD_READY Protogen task inputs.
All inputs are **required**

Name                     |       Default         |        Valid Values             |   Description
-------------------------|:---------------------:|---------------------------------|-----------------
raster                   |          N/A          | S3 URL   .TIF only              | S3 location of primary input .tif file.
slave                    |          N/A          | S3 URL   .TIF only              | S3 location of secondary input .tif file.

**OPTIONAL SETTINGS: Required = False**

* NA - No additional optional settings for this task exist


### Outputs

The following table lists the RAW Protogen task outputs.

Name | Required |   Description
-----|:--------:|-----------------
data |     Y    | This will explain the output file location and provide the primary output in .TIF format.
slave|     Y    | This will provide the secondary output in .TIF format.
log  |     N    | S3 location where logs are stored.

Each processed image will be written as .TIF image of data the same data type as its input and with the same number of bands as its input, and placed in the specified S3 Customer Location (e.g.  s3://gbd-customer-data/unique customer id/named directory/).  



### Advanced
To link the workflow of 1 input image into AOP_Strip_Processor into a protogen task you must use the follow GBDX tools script in python

```python
#First initalize the environment
#AOP strip processor has input values known to complete the Protogen tasks

from gbdxtools import Interface
gbdx = Interface()

post = "s3://receiving-dgcs-tdgplatform-com/055644448010_01_003"
pre  = "s3://receiving-dgcs-tdgplatform-com/055644447010_01_003"

aoptask1 = gbdx.Task('AOP_Strip_Processor', data=post, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image

aoptask2 = gbdx.Task('AOP_Strip_Processor', data=pre, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image

gluetask1 = gbdx.Task('gdal-cli')      
# move aoptask output to root where prototask can find it
gluetask1.inputs.data = aoptask1.outputs.data.value
gluetask1.inputs.execution_strategy = 'runonce'
gluetask1.inputs.command = """mv $indir/*/*.tif $outdir/"""

gluetask2 = gbdx.Task('gdal-cli')      
# move aoptask output to root where prototask can find it
gluetask2.inputs.data = aoptask2.outputs.data.value
gluetask2.inputs.execution_strategy = 'runonce'
gluetask2.inputs.command = """mv $indir/*/*.tif $outdir/"""

prototask = gbdx.Task('protogenV2CD_READY')
prototask.inputs.raster = gluetask1.outputs.data.value
prototask.inputs.slave  = gluetask2.outputs.data.value

workflow = gbdx.Workflow([aoptask1,aoptask2,gluetask1,gluetask2,prototask])
workflow.savedata(prototask.outputs.data,  'cdready/post')
workflow.savedata(prototask.outputs.slave, 'cdready/pre' )
workflow.execute()

workflow.status
```

### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Total Pixels   |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
| | | | |
| | | | |


###Known Issues
None

For background on the development and implementation of  Protogen  [Documentation under development](Insert link here)

###Contact Us
Tech Owner - Georgios Ouzounis - georgios.ouzounis@digitalglobe.com
Document Owner - Georgios Ouzounis - georgios.ouzounis@digitalglobe.com
